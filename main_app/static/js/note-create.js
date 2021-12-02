const dateInput = document.getElementById("id_date");

const picker = MCDatepicker.create({
  el: "#id_date",
  dateFormat: "yyyy-mm-dd",
  closeOnBlur: true,
  selectedDate: new Date(),
  theme: {
    theme_color: "#e0a470",
    main_background: "#ebd785",
  },
});

dateInput.addEventListener("click", (evt) => {
  picker.open();
});
