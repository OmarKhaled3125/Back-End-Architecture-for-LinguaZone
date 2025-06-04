document.addEventListener("DOMContentLoaded", () => {
    console.log("JavaScript loaded and DOM fully parsed.");

    // --- Common JWT Token (IMPORTANT: This should be handled securely, not hardcoded in production) ---
    const AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0OTA3NDk1MywianRpIjoiYTExYmJjYTItNDI1My00NWM4LWI5MTctOWUyMzkyMjIzYzFhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MjgsIm5iZiI6MTc0OTA3NDk1MywiY3NyZiI6IjRjNDBlZTA5LTMxNzQtNDczZC04MjQ4LTI3MmMwZGIyMTVhYyIsImV4cCI6MTc0OTExMDk1M30.Fs3_WfRyh-vaPk9Cw-adlIgpOOeKp7tiOjhIJuXz294";

    // --- Delete Operations ---
    const deleteButtons = document.querySelectorAll(".btn-danger[data-bs-toggle='modal']");
    deleteButtons.forEach(button => {
        button.addEventListener("click", () => {
            const endpoint = button.getAttribute("data-endpoint");
            const itemId = button.getAttribute("data-id");
            console.log(`Sending DELETE request to /api/general/${endpoint}/${itemId}`);

            const deleteModalBody = document.querySelector("#deleteConfirmationModal .modal-body strong");
            deleteModalBody.textContent = `ID: ${itemId}`;

            const confirmDeleteBtn = document.querySelector(".confirm-delete-btn");
            confirmDeleteBtn.onclick = () => {
                fetch(`/api/general/${endpoint}/${itemId}`, {
                    method: 'DELETE',
                    headers: {
                        "Authorization": `Bearer ${AUTH_TOKEN}`
                    }
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`Failed to delete item: ${response.statusText}`);
                    }
                    return response.json();
                })
                .then(data => {
                    alert(data.message || "Item deleted successfully");
                    location.reload();
                })
                .catch(error => {
                    console.error("Error deleting item:", error);
                    alert("An error occurred while deleting the item.");
                });
            };
        });
    });

    // --- Edit Operations ---
    const editButtons = document.querySelectorAll(".primary-btn[data-bs-toggle='modal']");
    editButtons.forEach(button => {
        button.addEventListener("click", async () => {
            const endpoint = button.getAttribute("data-endpoint");
            const itemId = button.getAttribute("data-id");
            console.log(`Fetching item data from /api/general/${endpoint}/${itemId}`);

            const editModal = document.querySelector("#editConfirmationModal");
            const editForm = editModal.querySelector("#editForm");
            const confirmEditButton = editModal.querySelector(".confirm-edit-btn");
            const modalTitle = editModal.querySelector("#editConfirmationModalLabel");

            // Reset form and hide all dynamic question fields
            editForm.reset();
            const editMcqOptions = editModal.querySelector("#editMcqOptions");
            const editFillBlankOptions = editModal.querySelector("#editFillBlankOptions");
            const editImageVideoOptions = editModal.querySelector("#editImageVideoOptions");
            const editChoicesContainer = editModal.querySelector("#editChoicesContainer");
            const currentMediaPreview = editModal.querySelector("#currentMediaPreview");

            editMcqOptions?.classList.add("d-none");
            editFillBlankOptions?.classList.add("d-none");
            editImageVideoOptions?.classList.add("d-none");
            if (editChoicesContainer) editChoicesContainer.innerHTML = '';
            if (currentMediaPreview) currentMediaPreview.innerHTML = '';

            // Dynamically set modal title
            modalTitle.textContent = `Edit ${endpoint.charAt(0).toUpperCase() + endpoint.slice(1)}`;

            try {
                const response = await fetch(`/api/general/${endpoint}/${itemId}`, {
                    method: 'GET',
                    headers: {
                        "Authorization": `Bearer ${AUTH_TOKEN}`
                    }
                });

                if (!response.ok) {
                    throw new Error(`Failed to fetch item data: ${response.statusText}`);
                }
                const itemData = await response.json();
                console.log("Fetched item data for edit:", itemData);

                if (endpoint === "question") {
                    const editQuestionTypeSelect = editModal.querySelector("#editQuestionTypeSelect");
                    editModal.querySelector("input[name='section_id']").value = itemData.section_id || '';
                    editQuestionTypeSelect.value = itemData.answer_type || '';
                    editModal.querySelector("textarea[name='question_content']").value = itemData.question_content || '';

                    const event = new Event('change');
                    editQuestionTypeSelect.dispatchEvent(event);

                    if (itemData.answer_type === "multiple_choice") {
                        if (itemData.choices && itemData.choices.length > 0) {
                            itemData.choices.forEach(choice => {
                                const choiceInputGroup = document.createElement("div");
                                choiceInputGroup.className = "input-group mb-3";
                                choiceInputGroup.innerHTML = `
                                    <input type="text" class="form-control" name="choices[]" placeholder="Choice Content" value="${choice.content || ''}" required>
                                    <div class="input-group-text">
                                        <input type="checkbox" name="is_correct[]" ${choice.is_correct ? 'checked' : ''}> Correct
                                        <button type="button" class="btn btn-danger btn-sm ms-2 remove-choice-btn">X</button>
                                    </div>
                                `;
                                editChoicesContainer.appendChild(choiceInputGroup);
                            });
                        } else {
                            addEmptyChoice(editChoicesContainer); // Add at least one empty choice if none exist
                        }
                    } else if (itemData.answer_type === "fill_in_blank") {
                        editModal.querySelector("input[name='correct_answer']").value = itemData.correct_answer || '';
                    } else if (itemData.answer_type === "image_video") {
                        if (itemData.media_url) {
                            currentMediaPreview.innerHTML = `
                                <p class="mt-2">Current Media:</p>
                                ${itemData.media_url.endsWith('.mp4') || itemData.media_url.endsWith('.webm') ?
                                    `<video controls height="100"><source src="${itemData.media_url}" type="video/mp4"></video>` :
                                    `<img src="${itemData.media_url}" alt="Current Media" class="img-thumbnail" height="100">`
                                }
                            `;
                        }
                    }

                    const addEditChoiceBtn = editModal.querySelector("#addEditChoiceBtn");
                    addEditChoiceBtn?.addEventListener("click", () => addEmptyChoice(editChoicesContainer));

                    editChoicesContainer?.addEventListener('click', (e) => {
                        if (e.target.classList.contains('remove-choice-btn')) {
                            e.target.closest('.input-group.mb-3').remove();
                        }
                    });

                    editQuestionTypeSelect.addEventListener("change", (event) => {
                        const selectedType = event.target.value;
                        editMcqOptions.classList.toggle("d-none", selectedType !== "multiple_choice");
                        editFillBlankOptions.classList.toggle("d-none", selectedType !== "fill_in_blank");
                        editImageVideoOptions.classList.toggle("d-none", selectedType !== "image_video");
                    });
                } else { // For level and section
                    editModal.querySelector("input[name='name']").value = itemData.name || '';
                    editModal.querySelector("textarea[name='description']").value = itemData.description || '';
                    if (endpoint === "level" && itemData.image_url) {
                        editModal.querySelector("input[name='image']").closest('.mb-3').innerHTML += `<small class="form-text text-muted">Current image: <img src="${itemData.image_url}" alt="Current Image" class="img-thumbnail" height="50"></small>`;
                    }
                }

                // Set the click handler for the confirm edit button
                confirmEditButton.onclick = async () => {
                    console.log("--- Edit Item button click initiated ---"); // NEW LOG
                    const formData = new FormData(editForm);
                    let payload;
                    let url = `/api/general/${endpoint}/${itemId}`;
                    let contentTypeHeader = "application/json";

                    if (endpoint === "question") {
                        const sectionId = formData.get("section_id");
                        const questionType = formData.get("question_type"); // This is 'answer_type' on the backend for questions

                        payload = {
                            section_id: parseInt(sectionId),
                            question_type: "text", // Fixed as per backend
                            answer_type: questionType,
                            question_content: formData.get("question_content"),
                        };
                        console.log(`Edit - Section ID: ${sectionId}, Question Type: ${questionType}`); // NEW LOG

                        if (questionType === "multiple_choice") {
                            const choices = [];
                            const choiceInputGroups = editForm.querySelectorAll("#editChoicesContainer .input-group.mb-3"); // Selecting each choice group

                            let hasCorrectChoice = false;

                            choiceInputGroups.forEach(group => {
                                const contentInput = group.querySelector("input[name='choices[]']");
                                const isCorrectCheckbox = group.querySelector("input[name='is_correct[]']");

                                const content = contentInput.value.trim();
                                if (!content) {
                                    alert("All choice contents must be filled for multiple-choice questions.");
                                    console.log("Edit - Error: Empty choice content found."); // NEW LOG
                                    throw new Error("Empty choice content"); // Stop submission
                                }
                                const isCorrect = isCorrectCheckbox.checked; // Direct check on the checkbox
                                if (isCorrect) hasCorrectChoice = true;
                                choices.push({
                                    choice_type: "text",
                                    content,
                                    is_correct: isCorrect,
                                });
                            });

                            console.log("Edit - Constructed choices array:", choices); // NEW LOG
                            console.log("Edit - Has at least one correct choice?", hasCorrectChoice); // NEW LOG

                            if (!hasCorrectChoice && choices.length > 0) {
                                alert("At least one correct choice is required for multiple-choice questions.");
                                console.log("Edit - Validation error: No correct choice."); // NEW LOG
                                return; // Stop submission
                            }
                            payload.choices = choices;
                        } else if (questionType === "fill_in_blank") {
                            const correctAnswer = formData.get("correct_answer");
                            if (!correctAnswer || !correctAnswer.trim()) {
                                alert("Correct answer is required for fill-in-the-blank questions.");
                                console.log("Edit - Error: Fill-in-blank answer missing."); // NEW LOG
                                return;
                            }
                            payload.correct_answer = correctAnswer;
                        } else if (questionType === "image_video") {
                            const mediaFile = formData.get("media");
                            if (mediaFile && mediaFile.name) {
                                const fileFormData = new FormData();
                                fileFormData.append("section_id", payload.section_id);
                                fileFormData.append("question_type", payload.question_type);
                                fileFormData.append("answer_type", payload.answer_type);
                                fileFormData.append("question_content", payload.question_content);
                                fileFormData.append("media", payload.media);
                                payload = fileFormData;
                                contentTypeHeader = undefined; // Let browser set multipart/form-data
                            } else {
                                payload = {
                                    section_id: parseInt(sectionId),
                                    question_type: "text",
                                    answer_type: questionType,
                                    question_content: formData.get("question_content"),
                                };
                            }
                        }
                        url = `/api/question/${itemId}`; // Adjust based on your Flask endpoint for updating questions
                        console.log("Sending PUT request for question with payload:", payload); // NEW LOG
                    } else { // For level and section
                        if (formData.get("image") && formData.get("image").name) {
                            payload = new FormData(editForm);
                            contentTypeHeader = undefined;
                        } else {
                            const jsonPayload = {};
                            formData.forEach((value, key) => {
                                if (key !== "image") {
                                    jsonPayload[key] = value;
                                }
                            });
                            payload = jsonPayload;
                        }
                        console.log("Sending PUT request for generic item with payload:", payload); // NEW LOG
                    }

                    try {
                        const fetchOptions = {
                            method: 'PUT',
                            headers: {
                                "Authorization": `Bearer ${AUTH_TOKEN}`
                            },
                            body: contentTypeHeader === "application/json" ? JSON.stringify(payload) : payload,
                        };

                        if (contentTypeHeader) {
                            fetchOptions.headers["Content-Type"] = contentTypeHeader;
                        }

                        const updateResponse = await fetch(url, fetchOptions);

                        if (!updateResponse.ok) {
                            const errorData = await updateResponse.json();
                            throw new Error(`Failed to update item: ${updateResponse.statusText} - ${errorData.message || ''}`);
                        }
                        const result = await updateResponse.json();
                        alert(result.message || "Item updated successfully");
                        location.reload();
                    } catch (error) {
                        console.error("Error updating item:", error);
                        alert("An error occurred while updating the item: " + error.message);
                    }
                };

            } catch (error) {
                console.error("Error fetching item data:", error);
                alert("An error occurred while fetching the item data: " + error.message);
            }
        });
    });

    // Helper function to add an empty choice input group for MCQs
    function addEmptyChoice(container) {
        const choiceInputGroup = document.createElement("div");
        choiceInputGroup.className = "input-group mb-3";
        choiceInputGroup.innerHTML = `
            <input type="text" class="form-control" name="choices[]" placeholder="Choice Content" required>
            <div class="input-group-text">
                <input type="checkbox" name="is_correct[]"> Correct
                <button type="button" class="btn btn-danger btn-sm ms-2 remove-choice-btn">X</button>
            </div>
        `;
        container.appendChild(choiceInputGroup);
    }

    // --- Add Item Logic ---

    // Attach event listener to the question type dropdown for Add Item modal
    const questionTypeSelect = document.getElementById("questionTypeSelect");
    const mcqOptions = document.getElementById("mcqOptions");
    const fillBlankOptions = document.getElementById("fillBlankOptions");
    const imageVideoOptions = document.getElementById("imageVideoOptions");
    const addChoiceBtn = document.getElementById("addChoiceBtn");
    const choicesContainer = document.getElementById("choicesContainer");

    if (questionTypeSelect) {
        questionTypeSelect.addEventListener("change", (event) => {
            const selectedType = event.target.value;
            console.log(`Selected question type (Add Modal): ${selectedType}`); // NEW LOG
            mcqOptions.classList.toggle("d-none", selectedType !== "multiple_choice");
            fillBlankOptions.classList.toggle("d-none", selectedType !== "fill_in_blank");
            imageVideoOptions.classList.toggle("d-none", selectedType !== "image_video");
            
            // Also ensure required attributes are correctly set based on visibility
            // Ensure inputs within hidden sections are not 'required' to avoid validation issues
            mcqOptions.querySelectorAll('input, textarea').forEach(el => el.required = (selectedType === "multiple_choice"));
            fillBlankOptions.querySelectorAll('input, textarea').forEach(el => el.required = (selectedType === "fill_in_blank"));
            imageVideoOptions.querySelectorAll('input, textarea').forEach(el => el.required = (selectedType === "image_video"));
        });
        questionTypeSelect.dispatchEvent(new Event('change')); // Trigger on load
    }

    // Add new choice for MCQ
    addChoiceBtn?.addEventListener("click", () => addEmptyChoice(choicesContainer));

    // Remove choice for MCQ
    choicesContainer?.addEventListener('click', (e) => {
        if (e.target.classList.contains('remove-choice-btn')) {
            e.target.closest('.input-group.mb-3').remove();
        }
    });

    // Attach event listener to the "Add New Item" button
    const addItemForm = document.getElementById("addItemForm");
    const confirmAddBtn = document.querySelector(".confirm-add-btn"); // Correctly selects the button by class

    if (confirmAddBtn) { // Always check if element exists
        confirmAddBtn.addEventListener("click", async () => {
            console.log("--- Add Question button click initiated ---"); // NEW LOG

            const formData = new FormData(addItemForm);
            const endpointHeaderElement = document.querySelector(".header-bar h2");
            if (!endpointHeaderElement) {
                alert("Could not determine endpoint from header.");
                console.log("Error: Endpoint header element not found."); // NEW LOG
                return;
            }
            const endpoint = endpointHeaderElement.textContent.split(" ")[0].toLowerCase();
            console.log(`Determined endpoint: ${endpoint} (for Add Item)`); // NEW LOG

            if (endpoint === "question") {
                const sectionId = formData.get("section_id");
                if (!sectionId) {
                    alert("Section ID is required to add a question.");
                    console.log("Error: Section ID is missing for question."); // NEW LOG
                    return;
                }
                console.log(`Section ID (Add): ${sectionId}`); // NEW LOG

                const questionType = formData.get("question_type"); // This is 'answer_type' on the backend for questions
                let payload;
                let contentTypeHeader = "application/json";

                if (questionType === "multiple_choice") {
                    const choices = [];
                    // NEW: More robust way to collect choices and their 'is_correct' status
                    const choiceInputGroups = addItemForm.querySelectorAll("#choicesContainer .input-group.mb-3");

                    let hasCorrectChoice = false;
                    for (const group of choiceInputGroups) {
                        const contentInput = group.querySelector("input[name='choices[]']");
                        const isCorrectCheckbox = group.querySelector("input[name='is_correct[]']");

                        const content = contentInput.value.trim();
                        if (!content) {
                            alert("All choice contents must be filled for multiple-choice questions.");
                            console.log("Error: Empty choice content found in add MCQ."); // NEW LOG
                            return; // Stop submission
                        }
                        const isCorrect = isCorrectCheckbox.checked; // Directly check the 'checked' property
                        if (isCorrect) hasCorrectChoice = true;
                        choices.push({
                            choice_type: "text", // Assuming all are text choices for now
                            content,
                            is_correct: isCorrect,
                        });
                    }

                    console.log("Add MCQ - Constructed choices array:", choices); // NEW LOG
                    console.log("Add MCQ - Has at least one correct choice?", hasCorrectChoice); // NEW LOG

                    if (!hasCorrectChoice && choices.length > 0) {
                        alert("At least one correct choice is required for multiple-choice questions.");
                        console.log("Add MCQ - Validation error: No correct choice selected."); // NEW LOG
                        return; // Stop submission
                    }

                    payload = {
                        section_id: parseInt(sectionId),
                        question_type: "text", // Fixed as per backend
                        answer_type: questionType,
                        question_content: formData.get("question_content"),
                        choices: choices
                    };

                } else if (questionType === "fill_in_blank") {
                    const correctAnswer = formData.get("correct_answer");
                    if (!correctAnswer || !correctAnswer.trim()) {
                        alert("Correct answer is required for fill-in-the-blank questions.");
                        console.log("Error: Fill-in-blank answer missing for add."); // NEW LOG
                        return;
                    }
                    payload = {
                        section_id: parseInt(sectionId),
                        question_type: "text",
                        answer_type: questionType,
                        question_content: formData.get("question_content"),
                        correct_answer: correctAnswer
                    };
                } else if (questionType === "image_video") {
                    const media = formData.get("media");
                    if (!media || !media.name) {
                        alert("Media file is required for image/video questions.");
                        console.log("Error: Media file missing for add."); // NEW LOG
                        return;
                    }
                    const fileFormData = new FormData();
                    fileFormData.append("section_id", sectionId);
                    fileFormData.append("question_type", "text");
                    fileFormData.append("answer_type", questionType);
                    fileFormData.append("question_content", formData.get("question_content"));
                    fileFormData.append("media", media);
                    payload = fileFormData;
                    contentTypeHeader = undefined;
                } else {
                    alert("Invalid question type selected.");
                    console.log(`Error: Invalid question type selected for add: ${questionType}`); // NEW LOG
                    return;
                }

                console.log("Payload being sent (Add Question):", payload); // NEW LOG

                try {
                    const fetchOptions = {
                        method: "POST",
                        headers: {
                            "Authorization": `Bearer ${AUTH_TOKEN}`
                        },
                        body: contentTypeHeader === "application/json" ? JSON.stringify(payload) : payload,
                    };

                    if (contentTypeHeader) {
                        fetchOptions.headers["Content-Type"] = contentTypeHeader;
                    }

                    console.log(`Sending POST to /api/question?section_id=${sectionId} with options:`, fetchOptions); // NEW LOG
                    const response = await fetch(`/api/question?section_id=${sectionId}`, fetchOptions);

                    if (response.ok) {
                        const result = await response.json();
                        alert(result.message || "Question added successfully!");
                        console.log("Question added successfully:", result); // NEW LOG
                        location.reload();
                    } else {
                        const error = await response.json();
                        console.error("Server error (Add Question):", error); // NEW LOG
                        alert(`Error: ${error.message}`);
                    }
                } catch (err) {
                    console.error("Error adding question:", err); // NEW LOG
                    alert("An error occurred while adding the question.");
                }
            } else { // Handle adding levels and sections
                let payload;
                let url = `http://127.0.0.1:5000/api/general/${endpoint}`;
                let contentTypeHeader = "application/json";

                const imageFile = formData.get("image");

                if (endpoint === "section") {
                    const levelIdInput = document.querySelector("#addItemForm input[name='level_id']");
                    if (!levelIdInput || !levelIdInput.value) {
                        alert("Level ID is required to create a section.");
                        console.log("Error: Level ID is missing for section."); // NEW LOG
                        return;
                    }
                    formData.set("level_id", parseInt(levelIdInput.value));
                }

                if (imageFile && imageFile.name) {
                    payload = formData;
                    contentTypeHeader = undefined;
                } else {
                    const jsonPayload = {};
                    formData.forEach((value, key) => {
                        if (key !== "image") {
                            jsonPayload[key] = value;
                        }
                    });
                    payload = jsonPayload;
                }

                console.log("Payload being sent (Add Level/Section):", payload); // NEW LOG

                try {
                    const fetchOptions = {
                        method: "POST",
                        headers: {
                            "Authorization": `Bearer ${AUTH_TOKEN}`
                        },
                        body: contentTypeHeader === "application/json" ? JSON.stringify(payload) : payload,
                    };

                    if (contentTypeHeader) {
                        fetchOptions.headers["Content-Type"] = contentTypeHeader;
                    }

                    console.log(`Sending POST to ${url} with options:`, fetchOptions); // NEW LOG
                    const response = await fetch(url, fetchOptions);

                    if (response.ok) {
                        const result = await response.json();
                        alert(result.message || "Item added successfully!");
                        console.log("Item added successfully:", result); // NEW LOG
                        location.reload();
                    } else {
                        const error = await response.json();
                        console.error("Server error (Add Level/Section):", error); // NEW LOG
                        alert(`Error: ${error.message}`);
                    }
                } catch (err) {
                    console.error("Error adding item (Level/Section):", err); // NEW LOG
                    alert("An error occurred while adding the item.");
                }
            }
        });
    } else {
        console.error("Error: '.confirm-add-btn' button not found when attaching listener."); // NEW LOG
    }
});