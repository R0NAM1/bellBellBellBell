const calendar = document.getElementById('calendar');
const yearLabel = document.getElementById('year-label');
let currentYear = new Date().getFullYear();

document.getElementById('prev-year').addEventListener('click', () => {
  currentYear--;
  generateCalendar(currentYear);
});

document.getElementById('next-year').addEventListener('click', () => {
  currentYear++;
  generateCalendar(currentYear);
});

function generateCalendar(year) {
  yearLabel.textContent = year;
  calendar.innerHTML = '';

  const monthNames = [
    'January', 'February', 'March', 'April', 'May', 'June', 
    'July', 'August', 'September', 'October', 'November', 'December'
  ];

  for (let month = 0; month < 12; month++) {
    const monthDiv = document.createElement('div');
    monthDiv.classList.add('month');

    const monthNameDiv = document.createElement('div');
    monthNameDiv.classList.add('month-name');
    monthNameDiv.textContent = monthNames[month];
    monthDiv.appendChild(monthNameDiv);

    const weekdaysDiv = document.createElement('div');
    weekdaysDiv.classList.add('weekdays');
    weekdaysDiv.innerHTML = '<span>Sun</span><span>Mon</span><span>Tue</span><span>Wed</span><span>Thu</span><span>Fri</span><span>Sat</span>';
    monthDiv.appendChild(weekdaysDiv);

    const daysDiv = document.createElement('div');
    daysDiv.classList.add('days');

    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    // Empty slots for days before the first day of the month
    for (let i = 0; i < firstDay; i++) {
      const emptySpan = document.createElement('span');
      daysDiv.appendChild(emptySpan);
    }

    // Days of the month
    for (let day = 1; day <= daysInMonth; day++) {
      const daySpan = document.createElement('span');
      daySpan.textContent = day;

      // Highlight today's date
      const today = new Date();
      if (year === today.getFullYear() && month === today.getMonth() && day === today.getDate()) {
        daySpan.classList.add('today');
      }

      daysDiv.appendChild(daySpan);
    }

    monthDiv.appendChild(daysDiv);
    calendar.appendChild(monthDiv);
  }
}

// Generate calendar for the current year initially
generateCalendar(currentYear);
