document.addEventListener("DOMContentLoaded", () => {
    const now = new Date();

    const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    const dayNames = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

    const currentDay = now.getDate();
    const currentMonth = now.getMonth();
    const currentYear = now.getFullYear();
    const currentDayOfWeek = now.getDay();

    document.getElementById("today-day").textContent = currentDay;
    document.getElementById("today-month-year").textContent = `${monthNames[currentMonth]} ${currentYear}`;
    document.getElementById("today-weekday").textContent = dayNames[currentDayOfWeek];
    document.getElementById("calendar-month-year").textContent = `${monthNames[currentMonth]} ${currentYear}`;
    const daysContainer = document.getElementById("calendar-days");
    daysContainer.innerHTML = "";

    const firstDayIndex = new Date(currentYear, currentMonth, 1).getDay();
    const totalDays = new Date(currentYear, currentMonth + 1, 0).getDate();

    let startOffset = firstDayIndex === 0 ? 6 : firstDayIndex - 1;

    for (let i = 0; i < startOffset; i++) {
        const emptySpan = document.createElement("span");
        daysContainer.appendChild(emptySpan);
    }

    for (let day = 1; day <= totalDays; day++) {
        const daySpan = document.createElement("span");
        daySpan.textContent = day;
        if (day === currentDay) {
            daySpan.classList.add("active");
        }

        daysContainer.appendChild(daySpan);
    }

    const editDate = document.getElementById("edit-date");
    const editTime = document.getElementById("edit-time");
    const editForm = document.getElementById("edit-form");
    const modal = document.getElementById("edit-modal");

    if (editDate) editDate.addEventListener("change", updateStatusBasedOnTime);
    if (editTime) editTime.addEventListener("change", updateStatusBasedOnTime);

    if (editForm) {
        editForm.addEventListener("submit", handleEditSubmit);
    }

    if (modal) {
        modal.addEventListener("click", (e) => {
            if (e.target === modal) {
                closeEditModal();
            }
        });
    }

    loadNotifications();
});

async function loadNotifications() {
    try {
        const response = await fetch("/get_notifications");
        const notifications = await response.json();

        const container = document.querySelector(".notifications-card");
        container.innerHTML = "";

        notifications.forEach((item) => {
            const card = document.createElement("div");
            card.classList.add("notification-item");

            const statusClass = item.status === "Sent" ? "status-sent" : "status-pending";

            const title = document.createElement("h4");
            title.textContent = item.name;

            const message = document.createElement("p");
            message.className = "notif-message";
            message.textContent = `💬 ${item.message || "—"}`;

            const meta = document.createElement("p");
            meta.textContent = `📅 ${item.date} | ⏰ ${item.time}`;

            const status = document.createElement("span");
            status.className = `status ${statusClass}`;
            status.textContent = item.status === "Sent" ? "✅ Sent" : "⏳ Pending";

            const actions = document.createElement("div");
            actions.style.marginTop = "8px";

            const editBtn = document.createElement("button");
            editBtn.type = "button";
            editBtn.className = "btn-edit";
            editBtn.textContent = "✏️ Edit";
            editBtn.addEventListener("click", () => openEditModal(item));

            const deleteForm = document.createElement("form");
            deleteForm.action = `/delete/${item.id}`;
            deleteForm.method = "POST";
            deleteForm.style.display = "inline";

            const deleteBtn = document.createElement("button");
            deleteBtn.type = "submit";
            deleteBtn.className = "btn-delete";
            deleteBtn.textContent = "🗑️ Sil";

            deleteForm.appendChild(deleteBtn);
            actions.appendChild(editBtn);
            actions.appendChild(deleteForm);

            card.appendChild(title);
            card.appendChild(message);
            card.appendChild(meta);
            card.appendChild(status);
            card.appendChild(actions);

            container.appendChild(card);
        });
    } catch (error) {
        console.error("Məlumat yüklənərkən xəta baş verdi:", error);
    }
}

function updateStatusBasedOnTime() {
    const dateInput = document.getElementById("edit-date");
    const timeInput = document.getElementById("edit-time");
    const statusSelect = document.getElementById("edit-status");

    if (!dateInput || !timeInput || !statusSelect) return;

    const selectedDate = dateInput.value;
    const selectedTime = timeInput.value;

    if (!selectedDate || !selectedTime) return;

    const selectedDateTime = new Date(`${selectedDate}T${selectedTime}`);
    const now = new Date();

    if (selectedDateTime <= now) {
        statusSelect.value = "Sent";
    } else {
        statusSelect.value = "Pending";
    }
}

function openEditModal(item) {
    const editId = document.getElementById("edit-id");
    const editName = document.getElementById("edit-name");
    const editMessage = document.getElementById("edit-message");
    const editDate = document.getElementById("edit-date");
    const editTime = document.getElementById("edit-time");
    const editStatus = document.getElementById("edit-status");

    if (editId) editId.value = item.id;
    if (editName) editName.value = item.name ?? "";
    if (editMessage) editMessage.value = item.message ?? "";
    if (editDate) editDate.value = item.date ?? "";
    if (editTime) editTime.value = item.time ?? "";
    if (editStatus) editStatus.value = item.status ?? "Pending";

    updateStatusBasedOnTime();

    const modal = document.getElementById("edit-modal");
    if (modal) {
        modal.style.display = "flex";
        modal.setAttribute("aria-hidden", "false");
        document.body.classList.add("modal-open");
    }
}

function closeEditModal() {
    const modal = document.getElementById("edit-modal");
    if (modal) {
        modal.style.display = "none";
        modal.setAttribute("aria-hidden", "true");
        document.body.classList.remove("modal-open");
    }
}

async function handleEditSubmit(e) {
    e.preventDefault();

    const id = document.getElementById("edit-id").value;
    const formData = new FormData();
    formData.append("notification_name", document.getElementById("edit-name").value);
    formData.append("notification_message", document.getElementById("edit-message").value);
    formData.append("notification_date", document.getElementById("edit-date").value);
    formData.append("notification_time", document.getElementById("edit-time").value);
    formData.append("notification_status", document.getElementById("edit-status").value);

    try {
        const response = await fetch(`/edit/${id}`, {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            throw new Error("Server xətası baş verdi");
        }

        closeEditModal();
        await loadNotifications();
    } catch (error) {
        console.error("Dəyişiklik yadda saxlanılarkən xəta:", error);
        alert("Yadda saxlanılarkən xəta baş verdi!");
    }
}
