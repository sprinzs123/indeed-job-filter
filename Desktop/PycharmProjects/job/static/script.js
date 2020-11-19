
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
            removeFields()
        });

    });
};
addFields()


// remove element on 'X' click. 
// need to put this function after add element so DOM knows new element exists
function removeFields(){
    let allRemoveBtns = document.querySelectorAll('.delete-btn')
    allRemoveBtns.forEach((removeBtn) => {
        console.log(removeBtn)
        removeBtn.addEventListener('click', function(event){
            let boxItem = removeBtn.parentElement
        })
    })
}
