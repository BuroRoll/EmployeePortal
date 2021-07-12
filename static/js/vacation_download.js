async function download_vacation() {
    let response = await fetch('/download_vacations_list/)', {
        method: 'GET'
    })
    console.log(response.ok)
}