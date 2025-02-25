// Открытие и закрытие модального окна
function openModal() {
    document.getElementById("busModal").style.display = "block";
}

function closeModal() {
    document.getElementById("busModal").style.display = "none";
}

// Показывает список автобусов в выбранной категории
function showBuses(category) {
    fetch(`/get_buses/${category}`)  // Запрос к серверу для получения автобусов категории
        .then(response => response.json())
        .then(data => {
            let busListContainer = document.getElementById("busListContainer");
            busListContainer.innerHTML = `<h3>Выберите автобус:</h3>`;
            
            let busList = document.createElement("ul");
            data.buses.forEach(bus => {
                let listItem = document.createElement("li");
                listItem.textContent = bus;
                listItem.className = "bus-item";
                listItem.onclick = () => showBusInfo(bus);
                busList.appendChild(listItem);
            });

            busListContainer.appendChild(busList);
        });
}

// Показывает информацию о выбранном автобусе
function showBusInfo(bus) {
    fetch(`/get_bus_info/${bus}`)  // Запрос к серверу
        .then(response => response.json())
        .then(data => {
            let busInfo = document.getElementById("busInfo");
            busInfo.innerHTML = `
                <h2>${data.name}</h2>
                <p>Вместимость: ${data.capacity}</p>
                <p>Описание: ${data.description}</p>
            `;
            closeModal();
        });
}