document.addEventListener("DOMContentLoaded", () => {
    const now = new Date();

    const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    const dayNames = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

    const currentDay = now.getDate();
    const currentMonth = now.getMonth();
    const currentYear = now.getFullYear();
    const currentDayOfWeek = now.getDay();

    const todayDayEl = document.getElementById("today-day");
    if (todayDayEl) todayDayEl.textContent = currentDay;

    const todayMonthYearEl = document.getElementById("today-month-year");
    if (todayMonthYearEl) todayMonthYearEl.textContent = `${monthNames[currentMonth]} ${currentYear}`;

    const todayWeekdayEl = document.getElementById("today-weekday");
    if (todayWeekdayEl) todayWeekdayEl.textContent = dayNames[currentDayOfWeek];

    const calendarMonthYearEl = document.getElementById("calendar-month-year");
    if (calendarMonthYearEl) calendarMonthYearEl.textContent = `${monthNames[currentMonth]} ${currentYear}`;

    const daysContainer = document.getElementById("calendar-days");
    if (daysContainer) {
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
    }

    const addForm = document.getElementById("add-form");
    if (addForm) {
        addForm.addEventListener("submit", handleAddSubmit);
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

async function handleAddSubmit(e) {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);

    try {
        const response = await fetch("/add", {
            method: "POST",
            body: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }
        });

        if (!response.ok) {
            throw new Error("Server xətası baş verdi");
        }

        form.reset();
        await loadNotifications();
    } catch (error) {
        console.error("Bildiriş əlavə edilərkən xəta:", error);
        alert("Bildiriş əlavə edilərkən xəta baş verdi!");
    }
}

async function loadNotifications() {
    try {
        const response = await fetch("/get_notifications");
        const notifications = await response.json();

        const container = document.querySelector(".notifications-card");
        if (!container) return;
        container.innerHTML = "";

        if (notifications.length === 0) {
            const emptyEl = document.createElement("div");
            emptyEl.className = "empty-state";
            emptyEl.innerHTML = `
                <span class="icon icon-bell empty-icon"></span>
                <p>No notifications scheduled yet.</p>
            `;
            container.appendChild(emptyEl);
            return;
        }

        notifications.forEach((item) => {
            const card = document.createElement("div");
            card.classList.add("notification-item");
            if (item.status === "Pending") card.classList.add("pending");

            const statusClass = item.status === "Sent" ? "status-sent" : "status-pending";
            const statusIcon = item.status === "Sent" ? "icon-sent" : "icon-pending";
            const statusLabel = item.status === "Sent" ? "Sent" : "Pending";

            card.innerHTML = `
                <div class="notif-header">
                    <h4>${item.name}</h4>
                    <span class="status ${statusClass}">
                        <span class="icon ${statusIcon}"></span> ${statusLabel}
                    </span>
                </div>
                <p class="notif-message">
                    <span class="icon icon-message"></span>
                    <span>${item.message || "—"}</span>
                </p>
                <div class="notif-meta">
                    <span><span class="icon icon-calendar"></span> ${item.date}</span>
                    <span><span class="icon icon-clock"></span> ${item.time}</span>
                </div>
                <div class="notif-actions">
                    <button type="button" class="btn-edit">
                        <span class="icon icon-edit"></span> Edit
                    </button>
                    <button type="button" class="btn-delete">
                        <span class="icon icon-delete"></span> Delete
                    </button>
                </div>
            `;

            // Attach event listeners
            const editBtn = card.querySelector(".btn-edit");
            if (editBtn) {
                editBtn.addEventListener("click", () => openEditModal(item));
            }

            const deleteBtn = card.querySelector(".btn-delete");
            if (deleteBtn) {
                deleteBtn.addEventListener("click", async () => {
                    if (confirm(`"${item.name}" bildirişini silmək istədiyinizdən əminsiniz?`)) {
                        try {
                            const delResponse = await fetch(`/delete/${item.id}`, {
                                method: "POST",
                                headers: {
                                    "X-Requested-With": "XMLHttpRequest"
                                }
                            });
                            if (delResponse.ok) {
                                await loadNotifications();
                            } else {
                                alert("Silinərkən xəta baş verdi");
                            }
                        } catch (err) {
                            console.error("Silmə xətası:", err);
                            alert("Silinərkən xəta baş verdi");
                        }
                    }
                });
            }

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
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }
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
