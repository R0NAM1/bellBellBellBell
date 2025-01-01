function onLoadFunction() {
    // Load current user editing as variable
    var path = window.location.pathname;

    var userEditing = path.split('/').filter(part => part).pop();

    var tittle = document.getElementById('tittle');
    tittle.innerText = 'Change Allowed Zones for ' + userEditing

    // Load list with all zones
    fetch('/settings/get_zones', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/text',
        },
        })
        .then(response => response.text())
        .then(data => {
        data = JSON.parse(data);
        console.log("Zone list from data /settings/get_zones", data)
        
        // Cont
        var zoneList = document.getElementById('zoneList');
        
        for (var zone of data) {
            var newZoneEntry = document.createElement('div')
            var newCheckbox = document.createElement('input');
            var newCheckboxLabel = document.createElement('h4');

            newCheckbox.type = 'checkbox';
            newCheckbox.id = zone;
            newCheckbox.style.padding = '15px';

            // Check if checkbox should already be checked
            console.log('Zones', window.userExitingZonesReturn)

            if (window.userExitingZonesReturn.includes(zone)) {
                console.log("Set to True: ", zone)
                newCheckbox.checked = true;
            }

            newCheckboxLabel.innerText = zone;
            newCheckboxLabel.style.padding = '15px';

            newZoneEntry.appendChild(newCheckbox);
            newZoneEntry.appendChild(newCheckboxLabel);

            newZoneEntry.style.display = 'inline-flex'
            newZoneEntry.style.justifyContent = 'center'

            zoneList.appendChild(newZoneEntry)
        }

        // Create submit and cancel buttons
        var acceptButton = document.createElement('button');
        var cancelButton = document.createElement('button');
        acceptButton.textContent = 'Accept';
        cancelButton.textContent = 'Cancel';
        acceptButton.style.padding = '5px';
        acceptButton.style.margin = '5px';
        acceptButton.style.marginRight = '25px';
        // acceptButton.style.position = 'absolute';
        // acceptButton.style.left = '25px';
        cancelButton.style.padding = '5px';
        cancelButton.style.margin = '5px';
        cancelButton.style.marginLeft = '25px';
        // cancelButton.style.position = 'absolute';
        // cancelButton.style.right = '25px';
        cancelButton.id = 'cancelButton';

        function cancel() {
            window.location.replace('/settings')
        }

        cancelButton.onclick = cancel;

        function accept() {
            // Need to create a new array based on checkboxes to send to server

            var finalArray = [];

            // Loop through using Zone list from server to check based on ID
            for (var zone of data) {
                var checkboxToCheck = document.getElementById(zone);
                if (checkboxToCheck.checked) {
                    // Add to final data array
                    finalArray.push(zone)
                }
            }

            // POST Request
            const subData = {
            submissionType: "changeUserZones",
            username: userEditing,
            newZones: JSON.stringify(finalArray)
            };

            // Make the POST request
            fetch('/settings', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(subData),
            })
            .then(response => {
                alert(response.status)
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

        acceptButton.onclick = accept;

        var innerbody = document.getElementById('innerbody');
        innerbody.appendChild(acceptButton);
        innerbody.appendChild(cancelButton);
        })
        .catch(error => {
            // console.error('Error:', error);
            alert(error)
        });
};




window.onload = onLoadFunction();