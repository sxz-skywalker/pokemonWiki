// 유효성 제약
const rules = {
    name: {
        presence: { allowEmpty: false, message: REQUIRED_MESSAGE }
    },
    email: {
        presence: { allowEmpty: false, message: REQUIRED_MESSAGE },
        email: { message: 'needs to be valid' }
    },
}

const myInfoWorker= {
    initialData: null,
    isfileChanged: false,
    init: async (user) => {
        myInfoWorker.initialData = user;
        $('#email').on('input', function() {
            // 숫자, @, ., 소문자, -, _ 만 남기기
            this.value = this.value.replace(/[^a-z0-9@.\-_]/g, '');
        });
        // 파일 첨부 버튼 초기화
        $('#file-add-btn').on('click', () => {
            $("#photo-file").click();
        });
        // 회원 정보 수정 버튼 초기화
        $('#submit-btn').on('click', (e) => {
            const data = myInfoWorker.getData();
            const result = myInfoWorker.validate(data, rules);
            if(result) {
                $('.error').addClass('hidden');
                myInfoWorker.update();
            }
        });
        // 파일 추가 이벤트
        $('#photo-file').on('change', function() {
            const file = this.files[0];
            if (file) {
                $('#photo-file-name').val(file.name);
                myInfoWorker.isfileChanged = true;
            }
        });
    },
    // 데이터 만들기
    getData: () => {
        return {
            name: $('#name').val(),
            email: $('#email').val(),
            school: $('#school').val(),
            'photo-file': $('#photo-file').val()
        };
    },
    // 유효성 검사
    validate: (data, rules) => {
        const errors = validate(data, rules);
        if (errors) {
            console.log('errors', errors);
            myInfoWorker.displayErrors(errors);
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
    // 회원 정보 수정
    update: async () => {
        let data = myInfoWorker.getData();
        try {
            // 파일 업로드
            if(myInfoWorker.isfileChanged) {
                const file_id = await myInfoWorker.uploadPhoto();
                if(!file_id) return;
                data = { ...data, file_id };
            }
            delete data['photo-file'];

            // 회원가입 API 호출
            const res = await updateUserProfile(data);
            if(res === 200) {
                location.href = '/users/my-info'
            }
        } catch (error) {
            console.error(error.message);
            alert('Modifiying info failed')
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