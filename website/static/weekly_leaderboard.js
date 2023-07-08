let currentSortColumnIndex = -1; // Track the currently sorted column index

window.addEventListener("DOMContentLoaded", () => {
  initializeSort();
});

function initializeSort() {
  const lastColumnIndex = getLastColumnIndex();
  sortTable(lastColumnIndex);
}

function getLastColumnIndex() {
  const thElements = document.querySelectorAll("#team-leaderboard-table th");
  return thElements.length - 1;
}

function sortTable(columnIndex) {
  const table = document.getElementById("team-leaderboard-table");
  const tbody = table.getElementsByTagName("tbody")[0];
  const rows = Array.from(tbody.getElementsByTagName("tr"));

  rows.sort((a, b) => {
    const cellA = parseInt(a.getElementsByTagName("td")[columnIndex].innerText);
    const cellB = parseInt(b.getElementsByTagName("td")[columnIndex].innerText);

    return cellB - cellA; // Compare as numbers in descending order
  });

  // Clear existing table rows
  while (tbody.firstChild) {
    tbody.removeChild(tbody.firstChild);
  }

  // Reappend sorted rows in descending order
  rows.forEach(row => {
    tbody.appendChild(row);
  });

  updateSortIndicator(columnIndex + 4);
  updateColumnBackground(columnIndex);
}

function sortTableResult(columnIndex) {
  const table = document.getElementById("team-leaderboard-table");
  const tbody = table.getElementsByTagName("tbody")[0];
  const rows = Array.from(tbody.getElementsByTagName("tr"));

  rows.sort((a, b) => {
    const cellA = a.getElementsByTagName("td")[columnIndex];
    const cellB = b.getElementsByTagName("td")[columnIndex];

    // Get the background color classes of the cells
    const classA = getBackgroundColorClass(cellA);
    const classB = getBackgroundColorClass(cellB);

    // Define the order of background color classes
    const classOrder = ["bg-light-green", "bg-light-yellow", "bg-light-red"];

    // Compare the classes using the order defined
    return classOrder.indexOf(classA) - classOrder.indexOf(classB);
  });

  // Clear existing table rows
  while (tbody.firstChild) {
    tbody.removeChild(tbody.firstChild);
  }

  // Reappend sorted rows in the new order
  rows.forEach(row => {
    tbody.appendChild(row);
  });

  updateSortIndicator(columnIndex + 4);
  updateColumnBackground(columnIndex);
}

function getBackgroundColorClass(element) {
  // Get the class list of the element
  const classList = element.classList;
  // Loop through the classes to find the background color class
  for (let i = 0; i < classList.length; i++) {
    const className = classList[i];
    if (className.startsWith("bg-light-")) {
      return className;
    }
  }
  return ""; // Return an empty string if no background color class is found
}

function updateSortIndicator(columnIndex) {
  const thElements = document.querySelectorAll("#team-leaderboard-table th");

  // Remove sort indicator from previous sorted column
  if (currentSortColumnIndex >= 0) {
    const previousSortTh = thElements[currentSortColumnIndex];
    previousSortTh.classList.remove("sort-desc");
  }

  // Add sort indicator to the current sorted column
  const currentSortTh = thElements[columnIndex];
  currentSortTh.classList.add("sort-desc");

  // Update the current sorted column index
  currentSortColumnIndex = columnIndex;
}

function updateColumnBackground(columnIndex) {
  const table = document.getElementById("team-leaderboard-table");
  const tbody = table.getElementsByTagName("tbody")[0];
  const rows = tbody.getElementsByTagName("tr");

  // Remove background color from all td elements
  for (let row of rows) {
    const cells = row.getElementsByTagName("td");
    for (let i = 0; i < cells.length; i++) {
      cells[i].classList.remove("sort-desc");
    }
  }

  // Add background color to the td elements in the current column
  for (let row of rows) {
    const cell = row.getElementsByTagName("td")[columnIndex];
    cell.classList.add("sort-desc");
  }
}

function sortTableAlphabetically(columnIndex) {
  const table = document.getElementById("team-leaderboard-table");
  const tbody = table.getElementsByTagName("tbody")[0];
  const rows = Array.from(tbody.getElementsByTagName("tr"));

  rows.sort((a, b) => {
    const cellA = a.getElementsByTagName("td")[columnIndex].innerText.toLowerCase();
    const cellB = b.getElementsByTagName("td")[columnIndex].innerText.toLowerCase();

    if (cellA < cellB) {
      return -1;
    } else if (cellA < cellB) {
      return 1;
    } else {
      return 0;
    }
  });

  // Clear existing table rows
  while (tbody.firstChild) {
    tbody.removeChild(tbody.firstChild);
  }

  // Reappend sorted rows in descending order
  rows.forEach(row => {
    tbody.appendChild(row);
  });

  updateSortIndicator(columnIndex);
  updateColumnBackground(columnIndex);
}

function sortTablePos(columnIndex) {
  const table = document.getElementById("team-leaderboard-table");
  const tbody = table.getElementsByTagName("tbody")[0];
  const rows = Array.from(tbody.getElementsByTagName("tr"));

  rows.sort((a, b) => {
    const cellA = parseInt(a.getElementsByTagName("td")[columnIndex].innerText);
    const cellB = parseInt(b.getElementsByTagName("td")[columnIndex].innerText);

    return cellA - cellB; // Compare as numbers in descending order
  });

  // Clear existing table rows
  while (tbody.firstChild) {
    tbody.removeChild(tbody.firstChild);
  }

  // Reappend sorted rows in descending order
  rows.forEach(row => {
    tbody.appendChild(row);
  });

  updateSortIndicator(columnIndex);
  updateColumnBackground(columnIndex);
}

function setHighestValueBackgroundColor(columnIndex, secondaryColumnIndex) {
  const table = document.getElementById("team-leaderboard-table");
  const tbody = table.getElementsByTagName("tbody")[0];
  const rows = Array.from(tbody.getElementsByTagName("tr"));

  // Find the cell with the highest value in the column
  let highestValue = Number.MIN_SAFE_INTEGER;
  let targetCell = null;
  let secondaryCell = null;
  let hasPositiveValue = false;

  rows.forEach(row => {
    const cellValue = parseInt(row.getElementsByTagName("td")[columnIndex].innerText);
    if (cellValue > highestValue) {
      highestValue = cellValue;
      targetCell = row.getElementsByTagName("td")[columnIndex];
      secondaryCell = row.getElementsByTagName("td")[secondaryColumnIndex];
    }
    if (cellValue > 0) {
      hasPositiveValue = true;
    }
  });

  // Add a class to the target cell for background color if columnIndex value is greater than 0
  if (targetCell !== null && hasPositiveValue && columnIndex > 0) {
    targetCell.classList.add("highest-value");
  }
  // Add a class to the secondary cell for background color
  if (secondaryCell !== null) {
    secondaryCell.classList.add("secondary-highest-value");
  }
}
function setHighestValueBackgroundColorTotal(columnIndex, secondaryColumnIndex) {
  const table = document.getElementById("team-leaderboard-table");
  const tbody = table.getElementsByTagName("tbody")[0];
  const rows = Array.from(tbody.getElementsByTagName("tr"));

  // Find the highest value in the column
  let highestValue = Number.MIN_SAFE_INTEGER;
  let targetCells = [];
  let secondaryCells = [];
  let hasPositiveValue = false;

  rows.forEach(row => {
    const cellValue = parseInt(row.getElementsByTagName("td")[columnIndex].innerText);
    if (cellValue > highestValue) {
      highestValue = cellValue;
      targetCells = [row.getElementsByTagName("td")[columnIndex]];
      secondaryCells = [row.getElementsByTagName("td")[secondaryColumnIndex]];
    } else if (cellValue === highestValue) {
      targetCells.push(row.getElementsByTagName("td")[columnIndex]);
      secondaryCells.push(row.getElementsByTagName("td")[secondaryColumnIndex]);
    }
    if (cellValue > 0) {
      hasPositiveValue = true;
    }
  });

  // Add a class to the target cells for background color if columnIndex value is greater than 0
  targetCells.forEach(cell => {
    if (cell !== null && hasPositiveValue && columnIndex > 0) {
      cell.classList.add("highest-value-total");
    }
  });

  // Add a class to the secondary cells for background color
  secondaryCells.forEach(cell => {
    if (cell !== null) {
      cell.classList.add("secondary-highest-value-total");
    }
  });
}





