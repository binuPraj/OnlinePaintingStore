console.log("JavaScript is working");

document.addEventListener('DOMContentLoaded', function () {
    const categoryField = document.getElementById('id_category');
    const subCategoryField = document.getElementById('id_sub_category');

    if (categoryField && subCategoryField) {
        categoryField.addEventListener('change', function () {
            const selectedCategoryId = categoryField.value;

            // Clear the subcategory dropdown
            subCategoryField.innerHTML = '<option value="">---------</option>';

            if (selectedCategoryId) {
                // Fetch subcategories based on the selected category
                fetch(`/get-subcategories/${selectedCategoryId}/`)
                    .then(response => response.json())
                    .then(data => {
                        data.subcategories.forEach(sub => {
                            const option = document.createElement('option');
                            option.value = sub.id;
                            option.textContent = sub.name;
                            subCategoryField.appendChild(option);
                        });
                    })
                    .catch(error => console.error('Error fetching subcategories:', error));
            }
        });
    }
});
