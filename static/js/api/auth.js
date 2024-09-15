// 로그인 API 호출
const loginUser = async (data) => {
    try {
        const response = await $.ajax({
            url: '/auth/login',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            cache: false
        });
        return response;  // 성공 시 리턴
    } catch (error) {
        console.error('Login failed:', error);
        throw error;  // 에러 발생 시 처리
    }
};

// 로그아웃 API 호출
const logoutUser = async () => {
    try {
        const response = await $.ajax({
            url: '/auth/logout',
            type: 'POST'
        });
        return response;  // 성공 시 리턴
    } catch (error) {
        console.error('failed:', error);
        throw error;  // 에러 발생 시 처리
    }
};

// 아이디 찾기 요청
const findId = async (email) => {
    try {
        const response = await $.ajax({
            url: '/auth/find-id',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                email
            }),
            cache: false
        });
        return response;  // 성공 시 200 리턴
    } catch (error) {
        console.error('failed:', error);
        throw error;
    }
};
// 비밀번호 찾기 요청
const findPassword = async (data) => {
    try {
        const response = await $.ajax({
            url: '/auth/find-pw',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            cache: false
        });
        return response;  // 성공 시 200 리턴
    } catch (error) {
        console.error('failed:', error);
        throw error;
    }
};