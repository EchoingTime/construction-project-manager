/*
@File Name: index.js
@Description: This file contains JavaScript functionality for the front-end of the web application. Specifically, it defines a 
function `deleteNote(noteId)` which sends a POST request to the backend to delete a note. Once the request is 
successfully processed, the page is reloaded to reflect the changes. This script is intended to enhance user 
interactivity and ensure real-time updates when managing notes.
@References
    - https://www.youtube.com/watch?v=dam0GPOAvVI&ab_channel=TechWithTim
    - ChatGPT for Detailed Description
*/

function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}