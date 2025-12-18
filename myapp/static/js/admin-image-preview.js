// Admin Image Preview on File Selection
document.addEventListener("DOMContentLoaded", function () {
  // Find all file inputs for images
  const fileInputs = document.querySelectorAll(
    'input[type="file"][accept*="image"]'
  );

  fileInputs.forEach(function (input) {
    // Skip if already has preview handler
    if (input.dataset.previewAdded) {
      return;
    }
    input.dataset.previewAdded = "true";

    // Use a mutable reference object so we can update it after input replacement
    const inputRef = { current: input };

    // Create preview container
    const previewContainer = document.createElement("div");
    previewContainer.className = "image-preview-container";
    previewContainer.style.cssText = "margin-top: 10px; display: none;";

    // Create preview image element
    const previewImg = document.createElement("img");
    previewImg.className = "image-preview-thumbnail";
    previewImg.style.cssText =
      "max-width: 200px; max-height: 200px; object-fit: cover; border-radius: 4px; border: 2px solid #e5e7eb; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);";
    previewImg.alt = "Preview";

    // Create remove preview button
    const removeBtn = document.createElement("button");
    removeBtn.type = "button";
    removeBtn.className = "image-preview-remove";
    removeBtn.innerHTML = "× Remove";
    removeBtn.style.cssText =
      "margin-left: 10px; padding: 5px 10px; background: #dc3545; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 12px;";

    previewContainer.appendChild(previewImg);
    previewContainer.appendChild(removeBtn);

    // Insert preview container after the file input's parent
    const inputWrapper = input.closest(".form-row") || input.parentElement;
    if (inputWrapper) {
      inputWrapper.appendChild(previewContainer);
    }

    // Show existing image if available (for edit forms)
    const existingImageInput = input
      .closest(".form-row")
      ?.querySelector('a[href*="media"]');
    if (existingImageInput) {
      const existingImg = document.createElement("img");
      existingImg.src = existingImageInput.href;
      existingImg.style.cssText =
        "max-width: 200px; max-height: 200px; object-fit: cover; border-radius: 4px; border: 2px solid #e5e7eb; margin-top: 10px; display: block;";
      existingImg.alt = "Current image";
      const existingContainer = document.createElement("div");
      existingContainer.className = "existing-image-container";
      existingContainer.style.cssText = "margin-top: 10px;";
      existingContainer.innerHTML =
        '<label style="display: block; margin-bottom: 5px; font-weight: 500;">Current Image:</label>';
      existingContainer.appendChild(existingImg);
      inputWrapper.appendChild(existingContainer);
    }

    // Handle file selection
    input.addEventListener("change", function (e) {
      const file = e.target.files[0];
      if (file) {
        // Validate image file
        if (!file.type.match("image.*")) {
          alert("Please select an image file.");
          inputRef.current.value = "";
          return;
        }

        // Create FileReader to preview
        const reader = new FileReader();
        reader.onload = function (e) {
          previewImg.src = e.target.result;
          previewContainer.style.display = "block";

          // Hide existing image container if present
          const existingContainer = inputWrapper.querySelector(
            ".existing-image-container"
          );
          if (existingContainer) {
            existingContainer.style.display = "none";
          }
        };
        reader.readAsDataURL(file);
      } else {
        previewContainer.style.display = "none";
      }
    });

    // Handle remove button
    removeBtn.addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();

      // Get current input from reference
      const currentInput = inputRef.current;

      // Method 1: Try to clear using value = '' first
      currentInput.value = "";

      // Method 2: If that doesn't work, replace the input completely
      // Store all input properties and get current parent (more reliable)
      const currentParent = currentInput.parentNode;
      const currentNextSibling = currentInput.nextSibling;

      if (!currentParent) {
        console.error("Cannot remove image: input parent not found");
        return;
      }

      const inputProps = {
        name: currentInput.name,
        id: currentInput.id,
        className: currentInput.className,
        accept: currentInput.accept,
        required: currentInput.required,
        multiple: currentInput.hasAttribute("multiple"),
        disabled: currentInput.hasAttribute("disabled"),
        parent: currentParent,
        nextSibling: currentNextSibling,
      };

      // Create a wrapper form to reset (trick to clear file input)
      const tempForm = document.createElement("form");
      tempForm.appendChild(currentInput.cloneNode(true));
      tempForm.reset();
      tempForm.remove();

      // Remove the original input
      currentInput.remove();

      // Create a brand new file input
      const newInput = document.createElement("input");
      newInput.type = "file";
      newInput.name = inputProps.name;
      if (inputProps.id) newInput.id = inputProps.id;
      if (inputProps.className) newInput.className = inputProps.className;
      if (inputProps.accept) newInput.accept = inputProps.accept;
      if (inputProps.required) newInput.required = inputProps.required;
      if (inputProps.multiple) newInput.setAttribute("multiple", "");
      if (inputProps.disabled) newInput.setAttribute("disabled", "");
      newInput.dataset.previewAdded = "true";

      // Insert the new input in the same position (with null check)
      if (inputProps.parent) {
        if (
          inputProps.nextSibling &&
          inputProps.nextSibling.parentNode === inputProps.parent
        ) {
          inputProps.parent.insertBefore(newInput, inputProps.nextSibling);
        } else {
          inputProps.parent.appendChild(newInput);
        }
      } else {
        // Fallback: use inputWrapper if parent is null
        if (inputWrapper) {
          inputWrapper.appendChild(newInput);
        } else {
          console.error("Cannot insert new input: no valid parent found");
          return;
        }
      }

      // Re-attach the change event listener
      newInput.addEventListener("change", function (e) {
        const file = e.target.files[0];
        if (file) {
          if (!file.type.match("image.*")) {
            alert("Please select an image file.");
            newInput.value = "";
            return;
          }
          const reader = new FileReader();
          reader.onload = function (e) {
            previewImg.src = e.target.result;
            previewContainer.style.display = "block";
            const existingContainer = inputWrapper.querySelector(
              ".existing-image-container"
            );
            if (existingContainer) {
              existingContainer.style.display = "none";
            }
          };
          reader.readAsDataURL(file);
        } else {
          previewContainer.style.display = "none";
        }
      });

      // Update the input reference for subsequent removals
      inputRef.current = newInput;

      // Hide preview
      previewContainer.style.display = "none";
      previewImg.src = "";

      // Show existing image container again if present
      const existingContainer = inputWrapper.querySelector(
        ".existing-image-container"
      );
      if (existingContainer) {
        existingContainer.style.display = "block";
      }

      // Force a change event
      setTimeout(function () {
        const changeEvent = new Event("change", {
          bubbles: true,
          cancelable: true,
        });
        newInput.dispatchEvent(changeEvent);
      }, 10);
    });
  });

  // Also handle inline forms (ProductImageInline)
  const inlineGroups = document.querySelectorAll(".inline-group");
  inlineGroups.forEach(function (group) {
    const inlineInputs = group.querySelectorAll(
      'input[type="file"][accept*="image"]'
    );
    inlineInputs.forEach(function (input) {
      if (input.dataset.previewAdded) {
        return;
      }
      input.dataset.previewAdded = "true";

      // Use a mutable reference object so we can update it after input replacement
      const inputRef = { current: input };

      const previewContainer = document.createElement("div");
      previewContainer.className = "image-preview-container-inline";
      previewContainer.style.cssText = "margin-top: 8px; display: none;";

      const previewImg = document.createElement("img");
      previewImg.className = "image-preview-thumbnail-inline";
      previewImg.style.cssText =
        "max-width: 120px; max-height: 120px; object-fit: cover; border-radius: 4px; border: 2px solid #e5e7eb; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);";
      previewImg.alt = "Preview";

      const removeBtn = document.createElement("button");
      removeBtn.type = "button";
      removeBtn.className = "image-preview-remove-inline";
      removeBtn.innerHTML = "×";
      removeBtn.style.cssText =
        "margin-left: 8px; padding: 3px 8px; background: #dc3545; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 11px; vertical-align: top;";

      previewContainer.appendChild(previewImg);
      previewContainer.appendChild(removeBtn);

      const inputRow = input.closest("tr") || input.parentElement;
      if (inputRow) {
        const cell = inputRow.querySelector("td:last-child") || inputRow;
        cell.appendChild(previewContainer);
      }

      input.addEventListener("change", function (e) {
        const file = e.target.files[0];
        if (file && file.type.match("image.*")) {
          const reader = new FileReader();
          reader.onload = function (e) {
            previewImg.src = e.target.result;
            previewContainer.style.display = "block";
          };
          reader.readAsDataURL(file);
        } else {
          previewContainer.style.display = "none";
        }
      });

      removeBtn.addEventListener("click", function (e) {
        e.preventDefault();
        e.stopPropagation();

        // Get current input from reference
        const currentInput = inputRef.current;

        // Clear the input value
        currentInput.value = "";

        // Store input properties and get current parent (more reliable)
        const currentParent = currentInput.parentNode;
        const currentNextSibling = currentInput.nextSibling;

        if (!currentParent) {
          console.error("Cannot remove image: input parent not found");
          return;
        }

        const inputProps = {
          name: currentInput.name,
          id: currentInput.id,
          className: currentInput.className,
          accept: currentInput.accept,
          required: currentInput.required,
          multiple: currentInput.hasAttribute("multiple"),
          disabled: currentInput.hasAttribute("disabled"),
          parent: currentParent,
          nextSibling: currentNextSibling,
        };

        // Create a wrapper form to reset (trick to clear file input)
        const tempForm = document.createElement("form");
        tempForm.appendChild(currentInput.cloneNode(true));
        tempForm.reset();
        tempForm.remove();

        // Remove the original input
        currentInput.remove();

        // Create a brand new file input
        const newInput = document.createElement("input");
        newInput.type = "file";
        newInput.name = inputProps.name;
        if (inputProps.id) newInput.id = inputProps.id;
        if (inputProps.className) newInput.className = inputProps.className;
        if (inputProps.accept) newInput.accept = inputProps.accept;
        if (inputProps.required) newInput.required = inputProps.required;
        if (inputProps.multiple) newInput.setAttribute("multiple", "");
        if (inputProps.disabled) newInput.setAttribute("disabled", "");
        newInput.dataset.previewAdded = "true";

        // Insert the new input in the same position (with null check)
        if (inputProps.parent) {
          if (
            inputProps.nextSibling &&
            inputProps.nextSibling.parentNode === inputProps.parent
          ) {
            inputProps.parent.insertBefore(newInput, inputProps.nextSibling);
          } else {
            inputProps.parent.appendChild(newInput);
          }
        } else {
          // Fallback: use inputRow if parent is null
          if (inputRow) {
            const cell = inputRow.querySelector("td:last-child") || inputRow;
            cell.appendChild(newInput);
          } else {
            console.error("Cannot insert new input: no valid parent found");
            return;
          }
        }

        // Re-attach the change event listener
        newInput.addEventListener("change", function (e) {
          const file = e.target.files[0];
          if (file && file.type.match("image.*")) {
            const reader = new FileReader();
            reader.onload = function (e) {
              previewImg.src = e.target.result;
              previewContainer.style.display = "block";
            };
            reader.readAsDataURL(file);
          } else {
            previewContainer.style.display = "none";
          }
        });

        // Update the input reference for subsequent removals
        inputRef.current = newInput;

        // Hide preview
        previewContainer.style.display = "none";
        previewImg.src = "";

        // Force a change event
        setTimeout(function () {
          const changeEvent = new Event("change", {
            bubbles: true,
            cancelable: true,
          });
          newInput.dispatchEvent(changeEvent);
        }, 10);
      });
    });
  });
});
