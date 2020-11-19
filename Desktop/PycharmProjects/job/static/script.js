
function addFields() {
    let allAddBtns = document.querySelectorAll('.filter-btn')
    allAddBtns.forEach((addField) => {
        addField.addEventListener('click', function (event){
            let parentDiv = addField.parentElement.parentElement
            let newItem = document.createElement('li');
            newItem.classList = 'one-box'
            let newField = `
                <input type="text" class='filter' placeholder="filter here">
                <button class='delete-btn'>X</button>
            `
            newItem.innerHTML = newField
            parentDiv.appendChild(newItem)
        });

    });
};
addFields()