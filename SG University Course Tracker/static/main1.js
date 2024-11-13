const selectedAll1 = document.querySelectorAll(".selected1");

selectedAll1.forEach((selected1) => {
  const optionsContainer1 = selected1.previousElementSibling;

  const optionsList1 = optionsContainer1.querySelectorAll(".option1");

  selected1.addEventListener("click", () => {
    if (optionsContainer1.classList.contains("active")) {
      optionsContainer1.classList.remove("active");
    } else {
      let currentActive1 = document.querySelector(".options-container1.active");

      if (currentActive1) {
        currentActive1.classList.remove("active");
      }

      optionsContainer1.classList.add("active");
    }


  });

  optionsList1.forEach((o) => {
    o.addEventListener("click", () => {
      selected1.innerHTML = o.querySelector("label").innerHTML;
      optionsContainer1.classList.remove("active");
    });
  });


  const filterList1 = (searchTerm) => {
    searchTerm = searchTerm.toLowerCase();
    optionsList1.forEach((option1) => {
      let label1 = option1.firstElementChild.nextElementSibling.innerText.toLowerCase();
      if (label.indexOf(searchTerm) != -1) {
        option1.style.display = "block";
      } else {
        option1.style.display = "none";
      }
    });
  };
});
