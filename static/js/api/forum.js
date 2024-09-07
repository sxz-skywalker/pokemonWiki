// 게시글 목록 가져오기
const getForumList = (query = '', searchType = 'title', page = 1, size = 10, onSuccess, onError) => {
    $.ajax({
        url: '/forums/list',
        type: 'GET',
        data: {
            query: query,       // 검색 쿼리
            type: searchType,   // 검색 타입
            page: page,
            size: size
        },
        success: onSuccess,
        error: onError
    });
};

// 게시글 상세 조회
const getForumDetail = (id, onSuccess, onError) => {
    $.ajax({
        url: `/forums/${id}`,
        type: 'GET',
        success: onSuccess,
        error: onError
    });
};

// 게시글 생성
const insertForum = (name, title, category, content, onSuccess, onError) => {
    $.ajax({
        url: '/forums',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            name: name,
            title: title,
            category: category,
            content: content
        }),
        success: onSuccess,
        error: onError
    });
};

// 게시글 수정
const updateForum = (id, name, category, title, content, onSuccess, onError) => {
    $.ajax({
        url: '/forums',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            id: id,
            name: name,
            category: category,
            title: title,
            content: content
        }),
        success: onSuccess,
        error: onError
    });
};

// 게시글 삭제
const deleteForum = (id, onSuccess, onError = () => {}) => {
    $.ajax({
        url: `/forums/${id}`,
        type: 'DELETE',
        success: onSuccess,
        error: onError
    });
};