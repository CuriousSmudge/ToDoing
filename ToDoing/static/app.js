const username = localStorage.getItem("username");
const password = localStorage.getItem("password");
const authHeader = "Basic " + btoa(username + ":" + password);

$( document ).ready(function() {
	tasks = $.ajax({
		type: "GET",
		url: "/tasks",
		headers: {
			Authorization: authHeader
		},
		success: function (response) {
			console.log("response recieved!!")
			console.log(response)
			add_tasks_to_dom(response)
		},
		error: function (response) {
			console.log("aaa oh nooo ooohhh oh by the way this is the response", response)
		}
	})

    $('#add_task').on('submit', function (event) {
        event.preventDefault();
        const task = $('#add_tasks').val()
        console.log(task)

        let t = $("#new_task")[0].value

        $.ajax({
            type: "POST",
            url: "/tasks",
            headers: {
                Authorization: authHeader
            },
            data: {
                "task": t
            },
            success: function (response) {
                console.log("yeah. mhm")
                console.log(response)
                location.reload()
            },
            error: function (response) {
                console.log("nonono", response)
            }
        })
    })
})


function add_tasks_to_dom(response) {
	for (i=0; i < response.length; i++) {
		let task = response[i]
		let text = task["task"]
        let id = task["id"]
		console.log(text, id)
		let completion = task["completed"]
		if (completion === 0) {
			$("#list").append("<li id='" + id + "' onclick='update_task_status(this)'>" + text + "</li>")
		}
		else {
			$("#list").append("<li id='" + id + "' onclick='update_task_status(this)' class=completed>" + text + "</li>")
		}
	}
}


function update_task_status(t) {
    $(t).click(function() {
        $(t).toggleClass("completed");
    });
    
    let completion = 0

    if (t.classList.contains("completed")) {
        let completion = 1
    }
    $.ajax({
        type: "GET",
        url: "/task_status",
        headers: {
            Authorization: authHeader
        },
        data: {
            "completion": completion,
            "id": t.id
        },
        success: function(response) {
            console.log("Completion Processed!")
            console.log(response)
        },
        error: function (response) {
            console.log("Completion Error: Not Processed")
            console.log(response)
        }
    });
}
