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