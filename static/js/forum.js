// 문서 타입
const DOC_TYPE = {
    CREATE: 'CREATE',
    UPDATE: 'UPDATE',
    READ: 'READ',
}

// 카테고리 정의
const categories = [
    {text: 'Information', value: 0},
    {text: 'Guides + Tips', value: 1},
    {text: 'Questions', value: 2},
    {text: 'Trades', value: 3},
]

// 검색 타입 정의
const searchTypes = [
    'title', 'content'
]

// 리스트 관리
const forumListWorker = {
    data: {
        page: 1,
        size: 5,
        cnt: 0,
        totalPages: 0,
        query: '',
        searchType: '',
    },
    // 포럼 리스트 페이지 초기화
    initForum: () => {
        // 검색 타입 초기화
        const optionHtml = `<option value=''>All</option>`
            + (searchTypes.map(e =>
                `<option value=${e}>${e}</option>`)).join('')
        $('#searchType').html(optionHtml);
        $('#query').on('input', (e) => {
            forumListWorker.data.query = e.target.value;
        });
        $('#searchType').on('change', (e) => {
            forumListWorker.data.searchType = e.target.value;
        });

        // 검색 기능 초기화
        $("form").on("submit", (event) => {
            event.preventDefault();
        });
        $('.search-btn').on('click', () => {
            forumListWorker.data.page = 1;
            forumListWorker.search();
        });

        // 검색 시작
        forumListWorker.search();
    },
    // 리스트 조회
    search: () => {
        getForumList(
            forumListWorker.data.query,
            forumListWorker.data.searchType,
            forumListWorker.data.page,
            forumListWorker.data.size,
            (res) => {
                forumListWorker.searchCallback(res);
            });
    },
    // 페이지로 리스트 조회
    searchByPage: (page) => {
        forumListWorker.data.page = page;
        forumListWorker.search();
    },
    // 리스트 조회 콜백
    searchCallback: (res) => {
        // 데이터 바인딩
        forumListWorker.data.cnt = res.cnt;
        forumListWorker.data.totalPages = res.total_pages;
        const hasResults = res.cnt > 0;

        // element 노출 / 비노출 설정
        const cntEl = $(".records");
        const createIcon = $(".create-icon-btn");
        $('.result-body').css('display', hasResults ? 'flex' : 'none');
        $('.no-result').css('display', hasResults ? 'none' : 'block');
        $('#pagination').css('display', hasResults ? 'flex' : 'none');
        $('.total-record').text(String(res.cnt).toLocaleString());
        forumListWorker.data.query && hasResults ? cntEl.show() : cntEl.hide();
        !forumListWorker.data.query && hasResults ? createIcon.show() : createIcon.hide();

        // HTML 그리기
        forumListWorker.makeHtmlTemplate(res.list);
        forumListWorker.updatePagination(res.page, res.total_pages);
    },
    // 리스트 조회 결과를 토대로 TR 엘리먼트 생성
    makeHtmlTemplate: (list) => {
        const template = $('#rowTemplate tbody').clone().html();
        const html = list?.map(e => {
            return template.replaceAll('#ID#', e.id)
                .replaceAll('#CATEGORY#', categories.find(v => v.value === e.category)?.text)
                .replaceAll('#CATEGORY_ID#', e.category)
                .replaceAll('#TITLE#', e.title)
                .replaceAll('#NAME#', e.name)
                .replaceAll('#CREATE_DATE#', moment(e.create_date).format('YYYY/MM/DD HH:mm:ss'))
        })
        $('.result-table').html(html.join(''));
    },
    // 페이징 업데이트
    updatePagination: (currentPage, totalPages) => {
        // 페이징 초기화
        $('#pagination').empty();
        // prev 버튼 추가
        $('#pagination').append(`
            <li class="page-item ${currentPage === 1 ? 'disabled' : ''}">
                <a class="page-link no-border" href="#" onclick="forumListWorker.searchByPage(${currentPage - 1})">«</a>
            </li>
        `);

        // 페이지 번호 추가
        Array.from({ length: totalPages }, (_, i) => i + 1).forEach(page => {
            $('#pagination').append(`
                <li class="page-item ${currentPage === page ? 'active' : ''}">
                    <a class="page-link no-border" href="#" onclick="forumListWorker.searchByPage(${page})">${page}</a>
                </li>
            `);
        });

        // next 버튼 추가
        $('#pagination').append(`
            <li class="page-item ${currentPage === totalPages ? 'disabled' : ''}">
                <a class="page-link no-border" href="#" onclick="forumListWorker.searchByPage(${currentPage + 1})">»</a>
            </li>
        `);
    },
}

// 상세 관리
const forumDetailWorker = {
    data: {
        id: undefined,
        name: '',
        title: '',
        content: '',
        category: '',
    },
    adjustDocType: (docType) => {
        $('.create-form-buttons button').hide();
        $('[data-type*="' + docType + '"]').show();
    },
    initForumDetail: (item, docType) => {
        // 문서 타입에 맞게 초기화
        forumDetailWorker.adjustDocType(docType);

        // 카테고리 초기화
        $('#category-select').html(categories.map(e =>
            `<option value=${e.value}>${e.text}</option>`))
        forumDetailWorker.data['category'] = categories[0].value;
        $('#category-select').on('change', (e) => {
            forumDetailWorker.data['category'] = e.target.value;
            forumDetailWorker.check();
        });

        // input 초기화
        $('#title, #content, #name').on('input, change', (e) => {
            forumDetailWorker.data[e.target.id] = e.target.value;
            forumDetailWorker.check();
        });

        // 버튼 초기화 - 글쓰기, 수정, 삭제
        $('#write-btn').on('click', () => {
            if(docType === DOC_TYPE.CREATE) {
                forumDetailWorker.addForum();
            } else {
                forumDetailWorker.editForum();
            }
        });

        $('#modify-btn').on('click', () => {
            forumDetailWorker.adjustDocType(DOC_TYPE.UPDATE);
            forumDetailWorker.changeReadAndWrite(false);
        });

        $('#delete-btn').on('click', () => {
            deleteForum(forumDetailWorker.data.id, (response) => {
                location.href = '/forums'
            }, (error) => {
                console.log('An error occurred while deleting', error);
            });
        });

        // 문서 타입에 따라 설정
        if(docType === DOC_TYPE.READ) {
            forumDetailWorker.changeReadAndWrite(true);
            forumDetailWorker.data = {
                ...item
            }
            $("#title").val(item.title);
            $("#name").val(item.name);
            $("#content").val(item.content);
            $("#category-select").val(item.category);
        } else {
            // 유효성 체크
            forumDetailWorker.check();
        }

    },
    // 읽기-쓰기 모드 변경
    changeReadAndWrite: (isRead) => {
        const els = $('.forum-detail input, .forum-detail textarea, .forum-detail select');
        els.attr('disabled', isRead);
        els.attr('placeholder', '');
    },
    // 유효성 체크
    check: () => {
        const isValid = forumDetailWorker.data.name &&
            forumDetailWorker.data.content && forumDetailWorker.data.title
        const el = $("#write-btn");
        isValid ? el.removeClass("disabled") : el.addClass("disabled")
    },
    // 글쓰기
    addForum: () => {
        insertForum(forumDetailWorker.data.name,
            forumDetailWorker.data.title,
            forumDetailWorker.data.category,
            forumDetailWorker.data.content, (res) => {
            if(res === 200) {
                location.href = '/forums'
            }
        }), (error) => {
            console.log('An error occurred while writing', error);
        };
    },
    // 수정하기
    editForum: () => {
        updateForum(forumDetailWorker.data.id,
            forumDetailWorker.data.name,
            forumDetailWorker.data.category,
            forumDetailWorker.data.title,
            forumDetailWorker.data.content, (res) => {
            if(res === 200) {
                forumDetailWorker.adjustDocType(DOC_TYPE.READ);
                forumDetailWorker.changeReadAndWrite(true);
            }
        }), (error) => {
            console.log('An error occurred while writing', error);
        };
    }
}

