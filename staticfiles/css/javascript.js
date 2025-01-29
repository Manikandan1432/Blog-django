function confirmBeforeDelete(url){
    var userConfirmed = confirm('Are you sure want to delete')
    if (userConfirmed) {
        window.location.href = url
    }
}