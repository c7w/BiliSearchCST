const search = () => {
    const type = document.getElementById('sel').value
    const content = document.getElementById("in").value
    if (!content) {
        if (type === 'video') {
            window.location.href = "/videoList"
        } else if (type === 'up') {
            window.location.href = "/upList"
        }
    } else {
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