import React, {Component} from 'react';
import './App.css';

// Importing Bulma as a CSS Framework from https://bulma.io/
import 'bulma/css/bulma.css';

//import task pages
import PointClickTask from './Task_Pages/PointClickTask';
import DragDropTask from './Task_Pages/DragDropTask';
import DrawingTask from './Task_Pages/DrawingTask';
import FollowBoxTask from "./Task_Pages/FollowBoxTask";
import NumberTypingTask from './Task_Pages/PatternTyping';
import MentalArithmetics from "./Task_Pages/MentalArithmetics";

export default class App extends Component {

    constructor(props) {
        super(props);

        this.state = {
            pageNumber: -99
        };

        this.tasks = [
            {name: "Mental Arithmetic Task", page: <MentalArithmetics toggleState={() => {this.toggleState(-99)}}/>},
            {name: "Point-and-Click Task", page: <PointClickTask toggleState={() => {this.toggleState(-99)}}/>},
            {name: "Drag-and-Drop Task", page: <DragDropTask toggleState={() => {this.toggleState(-99)}}/>},
            {name: "Drawing Task", page: <DrawingTask toggleState={() => {this.toggleState(-99)}}/>},
            {name: "Follow-Box Task", page: <FollowBoxTask toggleState={() => {this.toggleState(-99)}}/>},
            {name: "Typing Task", page: <NumberTypingTask toggleState={() => {this.toggleState(-99)}}/>},
        ];

    }


    toggleState(number) {
        this.setState(
            {pageNumber: number}
        )
    }

    renderTaskPage() {

        let pageToRender = this.tasks[this.state.pageNumber].page;

        return(
            <div>
                <div className="innerContainer">
                    {pageToRender}
                </div>
                <div className="small-screen">
                    <p>Your screen size is too small to view and try out the tasks. The minimum required size is a width of 950px and a height of 500px.
                        Please adjust your screen size to meet the necessary properties or use a different device.</p>
                </div>
            </div>
        );
    }

    renderIntroPage() {
        return(
            <div>
                <div className="section" style={{maxWidth: "1000px"}}>
                    <div className="content">
                        <h3>Task Demo App</h3><br/>
                        <h5>
                            In this demo app you can view all tasks as well as the stress manipulation task (mental
                            arithmetic task) used in the labratory experiment whose results are currently prepared to be
                            published in a research paper (name of project here).
                        </h5>
                        <h5>
                            All tasks contain an instruction (which was only used in the instruction condition). The tasks
                            themselves are identical with the tasks used in the high-stress and low-stress condition.
                        </h5>
                        <h5>
                            The mental arithmetic task only represents the stress manipulation used in the high-stress
                            condition. Here, the first 10 presented equations are shown.
                        </h5>
                        <h5>
                            The tasks also contain the mouse and keyboard logger. The logged data for each task are
                            viewed in the console after the task is over.
                        </h5>
                        <h5>
                            All tasks were only tested to work with recent versions of the Firefox or Chrome browser.
                            The tasks might not work as intended when viewed with another browser or an older version
                            of Firefox or Chrome. The tasks are intended to only work using the mouse and keyboard as input
                            devices. They are not intended to work on a smartphone or tablet. The window size of the task
                            is fixed and not responsive. All tasks can only be viewed in a window with a minimus width of
                            950px and a minimum height of 500px.
                        </h5>
                    </div>
                    <div className="content">
                        <h5 style={{textAlign: "left"}}>Select a task:</h5>
                        {
                            this.tasks.map((task, i) => (
                                <button
                                    style={{marginBottom: "3px"}}
                                    key={i}
                                    className="button is-medium is-fullwidth is-outlined is-info is-light"
                                    onClick={() => this.toggleState(i)}>{task.name}</button>
                            ))
                        }
                    </div>
                </div>
            </div>
        );

    }

    render() {
        return (
                <div className="outerContainer">
                    <div>
                       {this.state.pageNumber === -99 ? this.renderIntroPage(): this.renderTaskPage()}
                    </div>

                </div>
        );
    }

}
