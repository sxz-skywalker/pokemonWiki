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
        console.error('Logout failed:', error);
        throw error;  // 에러 발생 시 처리
    }
};