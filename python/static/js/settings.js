// Have settings be JS app instead of endpoints, still make sure user is admin

function resetMyPasswordConfirm() {
    var password = document.getElementById('password');
    var passwordConfirm = document.getElementById('passwordConfirm');

    // Verify all fields are populated.
    if (password.value == '') {
        alert("Please populate password field!")
    }
    else if (passwordConfirm.value == '') {
        alert("Please populate password confirm field!")
    }
    else {       
        // Veryify password fields match.
        if (password.value == passwordConfirm.value) {
            // Passwords match, gather data and make post request

            // POST Request
            const data = {
            submissionType: "selfResetPassword",
            password: password.value
            };

            // Make the POST request
            fetch(window.location.href, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
            })
            .then(response => {
                if (response.status == 200) {
                    alert('200 OK')
                }
            })
            .then(data => {
                // Press 'Cancel Button'
                var cancelButton = document.getElementById('cancelButton');
                cancelButton.click()
            })
            .catch(error => {
                // console.error('Error:', error);
                alert(error)
            });
            
        }
        else
        {
            alert("Passwords do not match, please verify!")
        }
    }
}

function changeUserZonePermissions() {
    // Redirect user to /settings/changezoneperms/<username>
    var userList = document.getElementById('userList');

    window.location.replace('/settings/changezoneperms/' + userList.value)
}

function resetUserPasswordConfirm() {
    var userList = document.getElementById('userList');
    var password = document.getElementById('password');
    var passwordConfirm = document.getElementById('passwordConfirm');

    // Verify all fields are populated.
    if (password.value == '') {
        alert("Please populate password field!")
    }
    else if (passwordConfirm.value == '') {
        alert("Please populate password confirm field!")
    }
    else {       
        // Veryify password fields match.
        if (password.value == passwordConfirm.value) {
            // Passwords match, gather data and make post request

            // POST Request
            const data = {
            submissionType: "userResetPassword",
            username: userList.value,
            password: password.value
            };

            // Make the POST request
            fetch(window.location.href, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
            })
            .then(response => {
                if (response.status == 200) {
                    alert('200 OK')
                }
            })
            .then(data => {
                // Press 'Cancel Button'
                var cancelButton = document.getElementById('cancelButton');
                cancelButton.click()
            })
            .catch(error => {
                // console.error('Error:', error);
                alert(error)
            });
            
        }
        else
        {
            alert("Passwords do not match, please verify!")
        }
    }
}

function deleteUserConfirm() {

    var userList = document.getElementById('userList');
    var confirmCheckbox = document.getElementById('confirmCheckbox');

    // Verify confirmCheckbox.
    if (confirmCheckbox.checked == true) {

            // POST Request
            const data = {
            submissionType: "userDelete",
            username: userList.value
            };

            // Make the POST request
            fetch(window.location.href, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
            })
            .then(response => {
                if (response.status == 200) {
                    alert('200 OK')
                }
            })
            .then(data => {
                // Press 'Cancel Button'
                var cancelButton = document.getElementById('cancelButton');
                cancelButton.click()
            })
            .catch(error => {
                // console.error('Error:', error);
                alert(error)
            });
            
    }
    else
    {
        alert("User not deleted, Confirm not checked.")
    }
    }

function addUserConfirm() {
    var userNameField = document.getElementById('userNameField');
    var passwordField = document.getElementById('passwordField');
    var passwordSureField = document.getElementById('passwordSureField');
    var isAdminBox = document.getElementById('isAdminBox');

    console.log(userNameField)
    console.log(userNameField.value)

    // Verify all fields are populated.
    if (userNameField.value == '') {
        alert("Please populate username field!")
    }
    else if (passwordField.value == '') {
        alert("Please populate password field!")
    }
    else if (passwordSureField.value == '') {
        alert("Please populate password verification field!")
    }
    else {       
        // Veryify password fields match.
        if (passwordField.value == passwordSureField.value) {
            // Passwords match, gather data and make post request

            // POST Request
            const data = {
            submissionType: "userAdd",
            username: userNameField.value,
            password: passwordField.value,
            isAdmin: isAdminBox.checked
            };

            // Make the POST request
            fetch(window.location.href, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
            })
            .then(response => {
                if (response.status == 200) {
                    alert('200 OK')
                }
            })
            .then(data => {
                // Press 'Cancel Button'
                var cancelButton = document.getElementById('cancelButton');
                cancelButton.click()
            })
            .catch(error => {
                // console.error('Error:', error);
                alert(error)
            });
            
        }
        else
        {
            alert("Passwords do not match, please verify!")
        }
    }
}

function createPopup(message, customhtml) {

    // Create blackout element and display empty popup window
    var blackoutElement = document.createElement('div');
    blackoutElement.style.opacity = '50%';
    blackoutElement.style.backgroundColor = 'black';
    blackoutElement.style.width = '100vw';
    blackoutElement.style.height = '100vh';
    blackoutElement.style.position = 'absolute';
    blackoutElement.style.top = '-100px';
    blackoutElement.style.zIndex = '99';

    var innerbody = document.getElementById('innerbody');
    innerbody.appendChild(blackoutElement);

    var popupElement = document.createElement("popupElement")
    popupElement.style.border = '5px solid black';
    popupElement.style.backgroundColor = '#b45100';
    popupElement.style.width = 'fit-content';
    popupElement.style.height = 'auto';
    popupElement.style.position = 'absolute';
    popupElement.style.top = '0';
    popupElement.style.zIndex = '199';
    popupElement.style.minWidth = '250px';
    popupElement.style.minHeight = '250px';
    popupElement.style.left = '0';
    popupElement.style.right = '0';
    popupElement.style.marginInline = 'auto';

    // Add Popup Message
    var popupMessage = document.createElement('h3');
    popupMessage.textContent = message;
    popupElement.appendChild(popupMessage)

    // Append customhtml
    popupElement.appendChild(customhtml)


    // Add buttons
    var acceptButton = document.createElement('button');
    var cancelButton = document.createElement('button');
    acceptButton.textContent = 'Accept';
    cancelButton.textContent = 'Cancel';
    acceptButton.style.bottom = '10px';
    acceptButton.style.position = 'absolute';
    acceptButton.style.left = '25px';
    cancelButton.style.bottom = '10px';
    cancelButton.style.position = 'absolute';
    cancelButton.style.right = '25px';
    cancelButton.id = 'cancelButton';

    function cancel() {
        popupElement.remove()
        blackoutElement.innerHTML = '';
        blackoutElement.remove()
    }

    cancelButton.onclick = cancel;

    // Depends on message
    if (message == 'Add New User') {
        acceptButton.onclick = addUserConfirm;
    }
    else if (message == 'Delete User') {
        acceptButton.onclick = deleteUserConfirm;
    }
    else if (message == 'Reset User Password') {
        acceptButton.onclick = resetUserPasswordConfirm;
    }
    else if (message == 'User Zone Permissions') {
        acceptButton.onclick = changeUserZonePermissions;
    }
    else if (message == 'Reset Your Password') {
        acceptButton.onclick = resetMyPasswordConfirm;
    }
    popupElement.appendChild(acceptButton);
    popupElement.appendChild(cancelButton);


    innerbody.appendChild(popupElement);

}

function runEventListeners() {

    // Admin event listeners
    var addUserElement = document.getElementById('Add User');
    addUserElement.addEventListener("click", (e) => {
        // Create popup content
        customContent = document.createElement('div');
        customContent.style.display = 'inline-grid'

        userNameField = document.createElement('input');
        passwordField = document.createElement('input');
        passwordSureField = document.createElement('input');
        makeUserAdminText = document.createElement('h3')
        isAdminBox = document.createElement('input')
        
        userNameField.id = 'userNameField';
        passwordField.id = 'passwordField';
        passwordSureField.id = 'passwordSureField';
        isAdminBox.id = 'isAdminBox';

        userNameField.type = 'text';
        passwordField.type = 'text';
        passwordSureField.type = 'text';
        isAdminBox.type = 'checkbox'
        
        userNameField.placeholder = 'Username';
        passwordField.placeholder = 'Password';
        passwordSureField.placeholder = 'Confirm Password';
        makeUserAdminText.textContent = 'Make User Admin?'

        customContent.appendChild(userNameField);
        customContent.appendChild(passwordField);
        customContent.appendChild(passwordSureField);
        customContent.appendChild(makeUserAdminText);
        customContent.appendChild(isAdminBox);

        // Create popup
        createPopup("Add New User", customContent)
      });

    // Delete user
    var deleteUserElement = document.getElementById('Delete User');
    deleteUserElement.addEventListener("click", (e) => {
          // Create popup content
          customContent = document.createElement('div');
          customContent.style.display = 'inline-grid';

          // Grab list of users from the server as array
          fetch('/settings/get_users', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/text',
            },
            })
            .then(response => response.text())
            .then(data => {
            data = JSON.parse(data);
            console.log("User list from data /settings/get_users", data)
            
            // Have user list, cont
            var userList = document.createElement('select');
            var confirmCheckbox = document.createElement('input');
            var areYouSure = document.createElement('h3')

            for (var name of data) {
                if (name !== 'admin') {
                    newOption = document.createElement('option');
                    newOption.value = name;
                    newOption.text = name;
                    userList.appendChild(newOption);
                }
            }

            userList.id = 'userList';
            confirmCheckbox.id = 'confirmCheckbox';
            confirmCheckbox.value = 'I am sure I want to delete this user.'
            confirmCheckbox.name = 'confirmcheckbox'
            areYouSure.textContent = 'Are you sure?';
    
            confirmCheckbox.type = 'checkbox';
            confirmCheckbox.style.width = '25px'
            confirmCheckbox.style.height = '25px'
            confirmCheckbox.style.position = 'relative'
            confirmCheckbox.style.left = '30%'
    
            customContent.appendChild(userList);
            customContent.appendChild(areYouSure);
            customContent.appendChild(confirmCheckbox);
    
            // Create popup
            createPopup("Delete User", customContent)

            })
            .catch(error => {
                // console.error('Error:', error);
                alert(error)
            });
        });

        // Audit Log
        var auditLogElement = document.getElementById('Audit Log');
        auditLogElement.addEventListener("click", (e) => {
          window.location.replace('/settings/auditlog')
        });

        // Reset a users password
        var resetUserElement = document.getElementById('Reset User Password');
        resetUserElement.addEventListener("click", (e) => {
          // Create popup content
          customContent = document.createElement('div');
          customContent.style.display = 'inline-grid';

          // Grab list of users from the server as array
          fetch('/settings/get_users', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/text',
            },
            })
            .then(response => response.text())
            .then(data => {
            data = JSON.parse(data);
            console.log("User list from data /settings/get_users", data)
            
            // Have user list, cont
            var userList = document.createElement('select');
            var password = document.createElement('input');
            var passwordConfirm = document.createElement('input')

            for (var name of data) {
                newOption = document.createElement('option');
                newOption.value = name;
                newOption.text = name;
                userList.appendChild(newOption);
            }

            userList.id = 'userList';
            password.id = 'password';
            passwordConfirm.id = 'passwordConfirm';

            password.type = 'text';
            passwordConfirm.type = 'text';

            password.placeholder = 'New Password';
            passwordConfirm.placeholder = 'Confirm Password';
    
            customContent.appendChild(userList);
            customContent.appendChild(password);
            customContent.appendChild(passwordConfirm);
    
            // Create popup
            createPopup("Reset User Password", customContent)

            })
            .catch(error => {
                // console.error('Error:', error);
                alert(error)
            });
        });

        // Change user zone permissions
        var resetUserElement = document.getElementById('User Zone Permissions');
        resetUserElement.addEventListener("click", (e) => {
          // Create popup content
          customContent = document.createElement('div');
          customContent.style.display = 'inline-grid';

          // Grab list of users from the server as array
          fetch('/settings/get_users', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/text',
            },
            })
            .then(response => response.text())
            .then(data => {
            data = JSON.parse(data);
            console.log("User list from data /settings/get_users", data)
            
            // Have user list, cont
            var userList = document.createElement('select');

            for (var name of data) {
                if (name !== 'admin') {
                    newOption = document.createElement('option');
                    newOption.value = name;
                    newOption.text = name;
                    userList.appendChild(newOption);
                }
            }
            userList.id = 'userList';

            customContent.appendChild(userList);
    
            // Create popup
            createPopup("User Zone Permissions", customContent)

            })
            .catch(error => {
                // console.error('Error:', error);
                alert(error)
            });
        });

// Change zone settings
var resetUserElement = document.getElementById('Change Zone Settings');
resetUserElement.addEventListener("click", (e) => {
  // Create popup content
  customContent = document.createElement('div');
  customContent.style.display = 'inline-grid';

  // Redirect to /settings/zoneedit
  window.location.replace('/settings/zoneedit')
});

// Change API settings
var resetUserElement = document.getElementById('Change API Settings');
resetUserElement.addEventListener("click", (e) => {
  // Create popup content
  customContent = document.createElement('div');
  customContent.style.display = 'inline-grid';

  // Redirect to /settings/apikeys
  window.location.replace('/settings/apikeys')
});

// Change Lockdown settings
var resetUserElement = document.getElementById('Lockdown Settings');
resetUserElement.addEventListener("click", (e) => {
  // Create popup content
  customContent = document.createElement('div');
  customContent.style.display = 'inline-grid';

  // Redirect to /settings/apikeys
  window.location.replace('/settings/lockdown')
});

// Change sounds settings
var resetUserElement = document.getElementById('sounds');
resetUserElement.addEventListener("click", (e) => {
  // Create popup content
  customContent = document.createElement('div');
  customContent.style.display = 'inline-grid';

  // Redirect to /settings/apikeys
  window.location.replace('/settings/sounds')
});

// USER SETTINGS

// Change my own password 
var resetUserElement = document.getElementById('userChangePassword');
resetUserElement.addEventListener("click", (e) => {
  // Create popup content
  customContent = document.createElement('div');
  customContent.style.display = 'inline-grid';

  var password = document.createElement('input');
  var passwordConfirm = document.createElement('input')

  password.id = 'password';
  passwordConfirm.id = 'passwordConfirm';

  password.type = 'text';
  passwordConfirm.type = 'text';

  password.placeholder = 'New Password';
  passwordConfirm.placeholder = 'Confirm Password';

  customContent.appendChild(password);
  customContent.appendChild(passwordConfirm);

  // Create popup
  createPopup("Reset Your Password", customContent)
});
}



function checkIfAdmin() {
    console.log("showAdminSettings", window.showAdminSettings)
    if (window.showAdminSettings == 'True') {
        // User is admin, show admin settings
        var adminElement = document.getElementById('adminSettings');
        adminElement.style.display = 'block';
    }


    runEventListeners()
}

document.onload = checkIfAdmin();