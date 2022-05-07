/*==================== MODALES ====================*/

// const modalViews = document.querySelectorAll(".services__modal");
const modalBtns = document.querySelectorAll(".trigger-modal");
const modalCloses = document.querySelectorAll(".services__modal-close");
const modalsDiv = document.querySelectorAll(".services__modal");
const modalsCont = document.querySelectorAll(".services__modal-content");
var bandClose = 0;

// Modal -> id ={nombremodal}
// trigger modal -> class="trigger-modal" href=#{nombremodal}


var idModal;

let modal = function (idModal) {
    document.getElementById(idModal).classList.add("active-modal");
};

modalBtns.forEach((modalBtn, i) => {
        modalBtn.addEventListener("click", () => {
        idModal = modalBtns[i].href.split('#')[1];
        // console.log(idModal);
        modal(idModal);
    });
});

modalCloses.forEach((modalClose) => {
    modalClose.addEventListener("click", () => {
        document.getElementById(idModal).classList.remove("active-modal");
    });
});

modalsCont.forEach((modalCont) => {
    modalCont.addEventListener("click", () => {
        bandClose = 1;
    });
});

modalsDiv.forEach((modalDiv) => {
    modalDiv.addEventListener("click", () => {
        if (bandClose == 0){
            if (modalDiv.classList.contains("active-modal")){
                modalDiv.classList.remove("active-modal");
            }
        }
        bandClose = 0;
    });
});
