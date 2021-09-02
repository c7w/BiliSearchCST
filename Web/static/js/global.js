const search = () => {
    const type = document.getElementById('sel').value
    let content = document.getElementById("in").value
    if (!content) {
        if (type === 'video') {
            window.location.href = "/videoList"
        } else if (type === 'up') {
            window.location.href = "/upList"
        }
    } else {
        content = encodeURI(content)
        window.location.href = `/search?type=${type}&keyword=${content}`
    }

}

const gotoPage = (base, maxV) => {
    const page = document.getElementById("page-input").value;

    const pageNum = Number(page);
    if (!pageNum || pageNum > maxV || pageNum < 1) {
        alert('请输入正确的页码范围!');
        return;
    }
    window.location.href = base + pageNum;
}

const InputKeyPress = (type, ...args) => {
    if (event.keyCode != 13) {
        return;
    }
    if (type === 'pagination') {
        gotoPage(args[0], args[1]);
    }
    else if (type === 'search') {
        search();
    }
}