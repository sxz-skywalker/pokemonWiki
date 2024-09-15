// 파일 업로드
const uploadFile = async (formData) => {
    try {
        const response = await $.ajax({
            url: '/files/upload',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false
        });
        return response.file_id;  // 파일 ID 리턴
    } catch (error) {
        throw new Error('File upload failed');
    }
};


// 파일 다운로드
const downloadFile = (fileId) => {
    $.ajax({
        url: `/files/download/${fileId}`,
        type: 'GET',
        xhrFields: {
            responseType: 'blob'  // 파일 데이터를 blob 형식으로 받음
        },
        success: (data, textStatus, xhr) => {
            const filename = xhr.getResponseHeader('Content-Disposition').split('filename=')[1].replace(/"/g, '');

            // 파일을 브라우저에서 다운로드 처리
            const url = window.URL.createObjectURL(data);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.append(a);
            a.click();
            window.URL.revokeObjectURL(url);
        },
    });
};