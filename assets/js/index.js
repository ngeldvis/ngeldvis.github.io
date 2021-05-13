$(document).ready(function() {

    $.ajax({
        url: '/get_projects',
        type: 'GET',
        data: {},
        success: (data) => {
            projects = JSON.parse(data);
            for(var i = 0; i < projects.length; i++) {
                project = projects[i];

                html = `
                <li class="project" id="project1">
                    <div class="list-item">
                        <img src="assets/images/${project.name}.png" alt="2048">
                        <div class="list-desc">
                            <h3>${camelCase_to_text(project.name)}</h3>
                            <p>${project.desc}</p>
                            <a href="${project.url}" target="_blank" class="repo-button" type="button">
                                View on GitHub
                            </a>
                            <ul class="topic-list">
                                ${'<li>'+project.topics.join('</li><li>')+'</li>'}
                            </ul> 
                        </div>
                    </div>
                </li>
                `;

                $('#pinned-projects').append(html);
            }
        },
        error: (e) => {
            console.log('error: ' + e.error);
        }
    });

});

function camelCase_to_text(str) {
    return str.replace(/[A-Z]/g, letter => ` ${letter}`)
}