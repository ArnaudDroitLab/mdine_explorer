document.body.onbeforeunload = function(event) {
    console.log("This message is printed in the browser console");
    try {
        let sessionData = sessionStorage.getItem('info-current-file-store');
        console.log("COucou toi");
        console.log(sessionData);
    } catch (error) {
        
        console.error("Une erreur s'est produite :", error);
    }
    
    let sessionData = sessionStorage.getItem('info-current-file-store');
    fetch('/close-session', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: sessionData
    }).then(response => response.json())
      .then(data => console.log(data))
      .catch((error) => console.error('Error:', error));
    return "Something"
};