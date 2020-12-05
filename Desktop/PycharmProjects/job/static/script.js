
function addFields() {
    let allAddBtns = document.querySelectorAll('.filter-btn')
    allAddBtns.forEach((addField) => {
        addField.addEventListener('click', function (event){
            let filterCount =getFilterNums(addField)
            let filerType = getColumnFilter(addField)
            let filterName = filerType + '-' + filterCount
            let parentDiv = addField.parentElement.parentElement
            let newItem = document.createElement('li');
            newItem.classList = 'one-box'
            let newField = `
                <input type="text" class='filter' placeholder="filter here" name='${filterName}'>
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
        removeBtn.addEventListener('click', function(event){
            let boxItem = removeBtn.parentElement.remove()
        })
    })
}


// get how many filters input recorded for each category
// need in creation of names for new filter inputs
function getFilterNums(childElement){
    let parentList = childElement.parentElement.parentElement
    return parentList.childElementCount
}


// determine to what column filter belongs to 
function getColumnFilter(childElement){
    let oneColumn = childElement.parentElement.parentElement
    return oneColumn.id
}


// form validation to make sure that url page is not empty
function formValidation(){
    let submitBtn = document.querySelector('.submit-btn')
    let emptyUrlError = document.querySelector('.empty-url')
    submitBtn.addEventListener('click', function(event){
        if(isUrlEmpty() == true){ 
            emptyUrlError.style.display = 'block'
            event.preventDefault()
        }
    })
}
formValidation()


// make sure that url is present
function isUrlEmpty(){
    let url_input = document.querySelector('#url-input').value
    if(url_input === ""){
        return true
    } else {
        return false
    }
}


