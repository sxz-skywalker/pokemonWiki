// ID 중복 확인
const checkId = (id, onSuccess, onError) => {
    $.ajax({
        url: '/users/check-id',
        type: 'GET',
        data: { id: id },
        success: onSuccess,
        error: onError
    });
};

// 회원가입
const signupUser = async (data) => {
    try {
        const response = await $.ajax({
            url: '/users/signup',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data)
        });
        return response;  // 성공 시 리턴
    } catch (error) {
        throw new Error('Signup failed');  // 에러 발생 시 처리
    }
};

// 프로필 수정
const updateUserProfile = async (data) => {
    try {
        const response = await $.ajax({
            url: '/users/profile',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data)
        });
        return response;  // 성공 시 리턴
    } catch (error) {
        throw new Error('Signup failed');  // 에러 발생 시 처리
    }
};