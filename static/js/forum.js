const DOC_TYPE = {
    CREATE: 'CREATE',
    UPDATE: 'UPDATE',
    READ: 'READ',
}

const categories = [
    {text: 'Information', value: 0},
    {text: 'Guides + Tips', value: 1},
    {text: 'Questions', value: 2},
    {text: 'Trades', value: 3},
]

const searchTypes = [
    'title', 'content'
]

const detail_data = {
    id: undefined,
    name: '',
    title: '',
    content: '',
    category: '',
}

const list_data = {
    page: 1,
    size: 5,
    cnt: 0,
    totalPages: 0,
    query: '',
    searchType: '',
}

const initForum = () => {
    search();
    // 검색 타입 초기화
    const optionHtml = `<option value=''>All</option>`
        + (searchTypes.map(e =>
            `<option value=${e}>${e}</option>`)).join('')
    $('#searchType').html(optionHtml);
    $('#query').on('input', (e) => {
        list_data.query = e.target.value;
    });
    $('#searchType').on('change', (e) => {
        list_data.searchType = e.target.value;
    });

    // 검색 초기화
    $("form").on("submit", (event) => {
      event.preventDefault();
    });
    $('.search-btn').on('click', () => {
        list_data.page = 1;
        search();
    })
}

// 검색
const search = () => {
    getForumList(
        list_data.query,
        list_data.searchType,
        list_data.page,
        list_data.size,
        (res) => {
            console.log('res', res);
            list_data.cnt = res.cnt;
            list_data.totalPages = res.total_pages;
            if(res.cnt === 0) {
                $(".result-body").hide();
                $(".no-result").show();
                return;
            }
            $(".result-body").show();
            $(".no-result").hide();
            const template = $('#rowTemplate tbody').clone().html();
            const html = res.list?.map(e => {
                return template.replaceAll('#ID#', e.id)
                    .replaceAll('#CATEGORY#', categories.find(v => v.value === e.category)?.text)
                    .replaceAll('#CATEGORY_ID#', e.category)
                    .replaceAll('#TITLE#', e.title)
                    .replaceAll('#NAME#', e.name)
                    .replaceAll('#CREATE_DATE#', moment(e.create_date).format('YYYY/MM/DD HH:mm:ss'))
            })
            $('.result-table').html(html.join(''));
            updatePagination(res.page, res.total_pages);
        });
}

const searchByPage = (page) => {
    list_data.page = page;
    search();
}

const updatePagination = (currentPage, totalPages) => {
    // 페이징 초기화
    $('#pagination').empty();
    // prev 버튼 추가
    $('#pagination').append(`
        <li class="page-item ${currentPage === 1 ? 'disabled' : ''}">
            <a class="page-link no-border" href="#" onclick="searchByPage(${currentPage - 1})">«</a>
        </li>
    `);

    // 페이지 번호 추가
    Array.from({ length: totalPages }, (_, i) => i + 1).forEach(page => {
        $('#pagination').append(`
            <li class="page-item ${currentPage === page ? 'active' : ''}">
                <a class="page-link no-border" href="#" onclick="searchByPage(${page})">${page}</a>
            </li>
        `);
    });

    // next 버튼 추가
    $('#pagination').append(`
        <li class="page-item ${currentPage === totalPages ? 'disabled' : ''}">
            <a class="page-link no-border" href="#" onclick="searchByPage(${currentPage + 1})">»</a>
        </li>
    `);
}

const adjustDocType = (docType) => {
    $('.create-form-buttons button').hide();
    $('[data-type*="' + docType + '"]').show();
}
const initForumDetail = (item, docType) => {
    // 문서 타입에 맞게 초기화
    adjustDocType(docType);

    // 카테고리 설정
    $('#category-select').html(categories.map(e =>
        `<option value=${e.value}>${e.text}</option>`))

    detail_data['category'] = categories[0].value;
    $('#category-select').on('change', (e) => {
        detail_data['category'] = e.target.value;
        check();
    });

    $('#title, #content, #name').on('input, change', (e) => {
        detail_data[e.target.id] = e.target.value;
        check();
    });

    $('#write-btn').on('click', () => {
        if(docType === DOC_TYPE.CREATE) {
            insertForum(detail_data.name, detail_data.title, detail_data.category, detail_data.content, (res) => {
                console.log('res', res)
                if(res === 200) {
                    location.href = '/forums'
                }
            }), (error) => {
                console.log('An error occurred while writing', error);
            };
        } else {
            updateForum(detail_data.id, detail_data.name, detail_data.category, detail_data.title, detail_data.content, (res) => {
                if(res === 200) {
                    adjustDocType(DOC_TYPE.READ);
                    changeReadAndWrite(true);
                }
            }), (error) => {
                console.log('An error occurred while writing', error);
            };
        }
    });
    $('#modify-btn').on('click', () => {
        adjustDocType(DOC_TYPE.UPDATE);
        changeReadAndWrite(false);
    });

    $('#delete-btn').on('click', () => {
        deleteForum(detail_data.id, (response) => {
            location.href = '/forums'
        }, (error) => {
            console.log('An error occurred while deleting', error);
        });
    });

    if(docType === DOC_TYPE.READ) {
        changeReadAndWrite(true);
        detail_data.id = item.id;
        detail_data.title = item.title;
        detail_data.content = item.content;
        detail_data.category = item.category;
        detail_data.name = item.name;
        $("#title").val(item.title);
        $("#name").val(item.name);
        $("#content").val(item.content);
        $("#category-select").val(item.category);
    } else {
        check();
    }

}

const changeReadAndWrite = (isRead) => {
    const els = $('.forum-detail input, .forum-detail textarea, .forum-detail select');
    els.attr('disabled', isRead);
    els.attr('placeholder', '');
}

const check = () => {
    const isValid = detail_data.name && detail_data.content && detail_data.title
    const el = $("#write-btn");
    isValid ? el.removeClass("disabled") : el.addClass("disabled")
}


// 포럼 리스트를 가져와 화면에 렌더링하는 함수
const loadForumList = () => {
    getForumList('', 'title', (data) => {
        console.log('Forum List:', data);
        // 데이터를 화면에 표시하는 로직 추가
    }, (error) => {
        console.log('Error fetching forum list:', error);
    });
};

// 새 포럼 글을 추가하는 함수
const createNewForumPost = () => {
    const name = $('#name').val();
    const title = $('#title').val();
    const content = $('#content').val();

    insertForum(name, title, content, (response) => {
        console.log('Insert Success:', response);
        // 성공적으로 글이 추가되었을 때, 목록 갱신 또는 알림
        loadForumList();
    }, (error) => {
        console.log('Error inserting forum post:', error);
    });
};

// 포럼 글 삭제
const deletePost = (id) => {
    deleteForum(id, (response) => {
        console.log('Delete Success:', response);
        // 삭제 후 목록 갱신
        loadForumList();
    }, (error) => {
        console.log('Error deleting post:', error);
    });
};