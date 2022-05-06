/*==================== MODALES ====================*/

// const modalViews = document.querySelectorAll(".services__modal");
const modalBtns = document.querySelectorAll(".trigger-modal");
const modalCloses = document.querySelectorAll(".services__modal-close");

// Modal -> id ={nombremodal}
// trigger modal -> class="trigger-modal" href=#{nombremodal}


var idModal;

let modal = function (idModal) {
    document.getElementById(idModal).classList.add("active-modal");
};

modalBtns.forEach((modalBtn, i) => {
        modalBtn.addEventListener("click", () => {
        idModal = modalBtns[i].href.substring(74);
        console.log(idModal);
        modal(idModal);
    });
});

modalCloses.forEach((modalClose) => {
    modalClose.addEventListener("click", () => {
        document.getElementById(idModal).classList.remove("active-modal");
    });
});
