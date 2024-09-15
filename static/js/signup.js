// 유효성 제약
const rules = {
    id: {
        presence: { allowEmpty: false, message: REQUIRED_MESSAGE },
        length: {
            minimum: 2,
            message: 'ID min 2 chars.'
        },
        isIdNotChecked: 'needs to be checked.', // custom validation',
        isIdDuplicated: 'is duplicated.' // custom validation
    },
    name: {
        presence: { allowEmpty: false, message: REQUIRED_MESSAGE }
    },
    password: {
        presence: { allowEmpty: false, message: REQUIRED_MESSAGE },
        length: {
            minimum: 8,
            message: 'min 8 chars.'
        }
    },
    'confirm-password': {
        presence: { allowEmpty: false, message: REQUIRED_MESSAGE },
        equality: {
            attribute: 'password',
            message: 'should be confirmed'
        }
    },
    email: {
        presence: { allowEmpty: false, message: REQUIRED_MESSAGE },
        email: { message: 'needs to be valid' }
    },
}

const signupWorker = {
    isIdNotChecked: true, // ID 중복 확인 여부
    isIdDuplicated: false, // ID 중복 여부
    init: () => {
        // 유효성 초기화
        signupWorker.initValidate();
        $('#id').on('input', function() {
            // 영어 소문자, 숫자만 남기기
            this.value = this.value.replace(/[^a-z0-9]/g, '');
        });
        $('#email').on('input', function() {
            // 숫자, @, ., 소문자, -, _ 만 남기기
            this.value = this.value.replace(/[^a-z0-9@.\-_]/g, '');
        });
        // ID 중복 확인 클릭 이벤트 초기화
        $('#check-id-btn').on('click', () => {
            signupWorker.checkId();
        });
        // 파일 첨부 버튼 초기화
        $('#file-add-btn').on('click', () => {
            $("#photo-file").click();
        });
        // 가입 버튼 초기화
        $('#submit-btn').on('click', (e) => {
            const data = signupWorker.getData();
            const result = signupWorker.validate(data, rules);
            if(result) {
                $('.error').addClass('hidden');
                signupWorker.signup();
            }
        });
        // 파일 추가 이벤트
        $('#photo-file').on('change', function() {
            const file = this.files[0];
            if (file) {
                $('#photo-file-name').val(file.name);
            }
        });
    },
    // 데이터 만들기
    getData: () => {
        return {
            id: $('#id').val(),
            name: $('#name').val(),
            password: $('#password').val(),
            'confirm-password': $('#confirm-password').val(),
            email: $('#email').val(),
            school: $('#school').val(),
            'photo-file': $('#photo-file').val()
        };
    },
    // ID 중복 확인
    checkId: () => {
        const id = $('#id').val();
        checkId(id, (res) => {
            const isValid = res === 200
            signupWorker.isIdNotChecked = false;
            signupWorker.isIdDuplicated = !isValid;
            const data = {
                id: $('#id').val(),
            };
            const result = signupWorker.validate(data, { id: rules.id });
        }), (error) => {
            console.log('An error occurred while checking id', error);
        };
    },
    // 유효성 초기화
    initValidate: () => {
        // validate 확장
        validate.validators.isIdNotChecked = () => signupWorker.isIdNotChecked ? rules.id.isIdNotChecked : null;
        validate.validators.isIdDuplicated = () => {
            if(!signupWorker.isIdDuplicated) {
                $(`#id-error span`).text('');
                $(`#id-error`).addClass('hidden');
                return;
            }
            return rules.id.isIdDuplicated;
        }
    },
    // 유효성 검사
    validate: (data, rules) => {
        const errors = validate(data, rules);
        if (errors) {
            console.log('errors', errors);
            signupWorker.displayErrors(errors);
            return false;
        }
        return true;
    },
    // 유효성 결과 노출
    displayErrors: (errors) => {
        $('.error').addClass('hidden');  // 기존 에러 메시지 숨기기
        Object.keys(errors).forEach((key) => {
            const errorMessage = errors[key][0];
            $(`#${key}-error span`).text(errorMessage);
            $(`#${key}-error`).removeClass('hidden');
        });
    },
    // 회원 가입
    signup: async () => {
        let data = signupWorker.getData();

        try {
            // 파일 업로드
            const file_id = await signupWorker.uploadPhoto();
            if(!file_id) return;
            data = { ...data, file_id };
            delete data['photo-file'];

            // 회원가입 API 호출
            const res = await signupUser(data);
            if(res === 200) {
                location.href = '/auth/login'
            }
        } catch (error) {
            console.error(error.message);
            alert('가입에 실패하였습니다.')
        }
    },
    // 사진 업로드
    uploadPhoto: async () => {
        const formData = new FormData();
        const file = $('#photo-file')[0].files[0];
        formData.append('file', file);
        return await uploadFile(formData);
    }
}