% rebase('layout.tpl', title='Home Page', year=year)

<div class="jumbotron">
    <h1>Queuing Systems and Population Dynamics</h1>
        <h3>Here you will find information about queuing systems and the modeling of death and reproduction processes in populations, analyzed using three examples <img src="static\images\star.png" width="25px" alt="star"></h3><br>
        
            <div class="little-question">
                <div>
                    <ul class="card-title-list">
                        <li><h3>What are queuing systems?</h3></li>
                    </ul>
                        <p>These are mathematical models that describe the processes of waiting and processing applications in various areas, from queues in stores and banks to computer servers and production lines. Such systems allow you to analyze how much time customers or tasks spend in a queue, how quickly they are serviced, and how to optimize the system to reduce waiting times and increase efficiency.</p><br>
                 </div>
                <img src="static\images\thinking.png" alt="Thinking man">
            </div>
        <ul class="card-title-list">
            <li><h3>Patterns of death and reproduction</h3></li>
        </ul>
        <p>These models are used to describe the dynamics of populations or groups of objects that can grow, die, or change their properties over time. In particular, they help to understand how the processes of reproduction, competition, death, and survival occur in ecosystems, social groups, or even at the cellular level. Such models make it possible to predict the development of systems, identify stable states, and make decisions to optimize them.</p><br>
        
        <p>On our website, you will find descriptions of modeling methods, implementation examples, and training materials that will help you better understand the principles of queuing systems and population dynamics <img src="static\images\heart.png" width="25px" alt="heart"></p>
</div>

<div class="cards-container">
    <a href="/wolf_island" class="card">
        <div class="cards">
            <img src="static\images\image_for_module1.png" alt="Wolves and Rabbits Illustration">
            <div class="card-content">
                <h3>The Model of Death and Reproduction</h3>
                <p>
                    A Markov process with discrete states on an NxM grid populated by rabbits and wolves. Rabbits randomly move or reproduce. She-wolves hunt rabbits for breeding. Wolves hunt rabbits, and in their absence, they hunt she-wolves, forming a chain of synchronous transitions.
                </p>
            </div>
        </div>
    </a>

    <a href="/infection_spread" class="card">
        <div class="cards">
            <img src="static\images\image_for_module2.png" alt="Ringworm Infection Illustration">
            <div class="card-content">
                <h3>The Model of Ringworm Infection Spread</h3>
                <p>
                    A Markov process with discrete states on a grid. Each cell goes to the next state in one step: the living one dies if it has < a or > b neighbors, otherwise it survives; the dead one comes to life when the neighbors a and b are set by the user. All cells are updated synchronously, forming a chain of transitions.
                </p>
            </div>
        </div>
    </a>

    <a href="/cells_colonies" class="card">
        <div class="cards">
            <img src="static\images\image_for_module3.png" alt="Colonies of Living Cells Grid">
            <div class="card-content">
                <h3>The Life of Generations of Colonies of Living Cells</h3>
                <p>
                    A Markov process with discrete states on an NxN grid. The central cell is initially infected. Each infected cell has a 0.5 probability of infecting neighboring healthy cells in one time step. After 6 steps, the infected cell becomes immune for 4 steps, then returns to a healthy state.
                </p>
            </div>
        </div>
    </a>
</div>