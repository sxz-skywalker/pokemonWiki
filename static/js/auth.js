const rules = {
    id: {
        presence: { allowEmpty: false, message: REQUIRED_MESSAGE },
        length: {
            minimum: 2,
            message: 'ID min 2 chars.'
        },
    },
    password: {
        presence: { allowEmpty: false, message: REQUIRED_MESSAGE },
        length: {
            minimum: 8,
            message: 'min 8 chars.'
        },
    },
    login: {
        checkFailed: 'failed.'
    }
}

const authWorker = {
    isLoginFailed: false,
    init: () => {
        authWorker.initValidate();
        // 유효성 초기화
        $('#id').on('input', function() {
            // 영어 소문자, 숫자만 남기기
            this.value = this.value.replace(/[^a-z0-9]/g, '');
        });
        // 로그인 버튼 초기화
        $('#submit-btn').on('click', (e) => {
            const data = authWorker.getData();
            const result = authWorker.validate(data, rules);
            if(result) {
                $('.error').addClass('hidden');
                authWorker.login();
            }
        });
    },
    getData: () => {
        return {
            id: $('#id').val(),
            password: $('#password').val(),
        };
    },
    // 유효성 초기화
    initValidate: () => {
        // validate 확장
        validate.validators.checkFailed = () => authWorker.isLoginFailed ? rules.login.checkFailed : '';
    },
    validate: (data, rules) => {
        console.log('data', data)
        const errors = validate(data, rules);
        if (errors) {
            console.log('errors', errors);
            authWorker.displayErrors(errors);
            return false;
        }
        return true;
    },
    displayErrors: (errors) => {
        $('.error').addClass('hidden');  // 기존 에러 메시지 숨기기
        Object.keys(errors).forEach((key) => {
            const errorMessage = errors[key][0];
            $(`#${key}-error span`).text(errorMessage);
            $(`#${key}-error`).removeClass('hidden');
        });
    },
    login: async () => {
        let data = authWorker.getData();
        try {
            // 로그인 API 호출
            const res = await loginUser(data);
            const isSucceed = res === 200
            authWorker.isLoginFailed = !isSucceed;
            authWorker.validate({
                login: isSucceed
            }, { login: rules.login });
            if(res === 200) {
                location.href='/pokemons';
            }
        } catch (error) {
            console.error(error.message);
        }
    },
}