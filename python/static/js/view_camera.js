var rightPopup = false;
var timer = null;

// Register back button
document.addEventListener('mousemove', function() {
    var rightDashButton = document.getElementById('right-dash-button');

    document.body.classList.remove('hide-cursor');
    clearTimeout(timer);
    document.getElementById('exitButton').style.display = 'block';
    rightDashButton.style.display = 'block';

    timer = setTimeout(function() {
        // When mouse has not moved for one second
        document.body.classList.add('hide-cursor');
        document.getElementById('exitButton').style.display = 'none';
        rightDashButton.style.display = 'none';
    }, 1000);
});

// Add event listener for right side
var rightButton = document.getElementById('collapseButton');
var rightDash = document.getElementById('right-dash');
var rightDashButton = document.getElementById('right-dash-button');

rightButton.addEventListener('click', function() {
    
    var rightButton = document.getElementById('collapseButton');
    if (rightPopup == false) {
        rightButton.style.transform = 'scaleX(-1)';
        rightDash.style.display = 'none';
        rightDashButton.style.right = '0px';
        rightPopup = true;
    }
    else {
        rightButton.style.transform = 'scaleX(1)';
        rightDash.style.display = 'block';
        rightDashButton.style.right = '362px';
        rightPopup = false;
    }
   
});

rightButton.click()
