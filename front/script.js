let currentMonth = new Date().getMonth() + 1; 
let currentYear = new Date().getFullYear();

function updateCalendar() {
    document.getElementById('current-month-year').textContent = 
        `${new Date(currentYear, currentMonth - 1).toLocaleString('default', { month: 'long' })} ${currentYear}`;

    fetch(`http://localhost:5000/api/events?month=${currentMonth}&year=${currentYear}`)
        .then(response => response.json())
        .then(data => {
            renderCalendar(data);
        })
        .catch(error => console.error('Error fetching events:', error));
}

function renderCalendar(events) {
    const calendarElement = document.getElementById('calendar');
    calendarElement.innerHTML = '';

    const firstDay = new Date(currentYear, currentMonth - 1, 1);
    const lastDay = new Date(currentYear, currentMonth, 0);
    const daysInMonth = lastDay.getDate();
    const startDay = firstDay.getDay();

    const days = document.createElement('div');
    days.classList.add('days');

    const dayNames = ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek', 'Sobota', 'Niedziela'];
    dayNames.forEach(dayName => {
        const dayNameElement = document.createElement('div');
        dayNameElement.classList.add('day-name');
        dayNameElement.textContent = dayName;
        days.appendChild(dayNameElement);
    });

    const emptyDaysBefore = (startDay === 0 ? 6 : startDay - 1);
    for (let i = 0; i < emptyDaysBefore; i++) {
        const emptyDayElement = document.createElement('div');
        emptyDayElement.classList.add('day', 'not-current-month');
        days.appendChild(emptyDayElement);
    }

    const today = new Date().getDate(); 

    for (let day = 1; day <= daysInMonth; day++) {
        const dayElement = document.createElement('div');
        dayElement.classList.add('day');

        
        if (day === today && currentMonth === new Date().getMonth() + 1 && currentYear === new Date().getFullYear()) {
            dayElement.classList.add('current-day'); 
        }

        dayElement.textContent = day;

        const eventsOnDay = events.filter(event => {
            const eventStart = new Date(event.start);
            const eventEnd = new Date(event.end);
            return eventStart.getDate() <= day && eventEnd.getDate() >= day && 
                   eventStart.getMonth() === (currentMonth - 1) && 
                   eventStart.getFullYear() === currentYear;
        });

        eventsOnDay.forEach(event => {
            const eventTitle = document.createElement('div');
            eventTitle.textContent = event.title;
            eventTitle.classList.add('event-title');
            eventTitle.dataset.id = event.id;

            eventTitle.addEventListener('click', () => {
                fetchEventDetails(event.id);
            });

            dayElement.appendChild(eventTitle);
            dayElement.classList.add('event-day');
        });

        days.appendChild(dayElement);
    }

    calendarElement.appendChild(days);
}

function fetchEventDetails(eventId) {
    fetch(`http://localhost:5000/api/events/${eventId}`)
        .then(response => response.json())
        .then(data => {
            showEventDetails(data);
        })
        .catch(error => console.error('Error fetching event details:', error));
}

function showEventDetails(event) {
    const modal = document.createElement('div');
    modal.classList.add('modal');
    modal.innerHTML = `
        <div class="modal-content">
            <span class="close-button">&times;</span>
            <h2>${event.name}</h2>
            <p><strong>Początek:</strong> ${new Date(event.start_time).toLocaleString()}</p>
            <p><strong>Czas trwania:</strong> ${event.duration} dni</p>
            <p><strong>Lokalizacja:</strong> ${event.location}</p>
            <p><strong>Opis:</strong> ${event.short_description}</p>
            <p><strong>Szczegóły:</strong> ${event.long_description}</p>
            <p><a href="${event.registration_link}" target="_blank">Rejestracja</a></p>
        </div>
    `;
    document.body.appendChild(modal);

    modal.querySelector('.close-button').addEventListener('click', () => {
        document.body.removeChild(modal);
    });
}

document.getElementById('prev-month').addEventListener('click', () => {
    if (currentMonth === 1) {
        currentMonth = 12;
        currentYear -= 1;
    } else {
        currentMonth -= 1;
    }
    updateCalendar();
});

document.getElementById('next-month').addEventListener('click', () => {
    if (currentMonth === 12) {
        currentMonth = 1;
        currentYear += 1;
    } else {
        currentMonth += 1;
    }
    updateCalendar();
});

updateCalendar();
