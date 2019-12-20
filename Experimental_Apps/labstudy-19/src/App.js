/*
Experimental React App used in the study
This is js file that controls the experimental flow
All other components in the folders are the files for dedicated experimental pages used in the experiment (e.g.
mouse task page, questionnaire page, etc..

This app was build to fit the purpose of the study and should not be interpreted as a state-of-the-art general
solution to build experimental web applications.

For feedback, better solutions or questions regarding the experimental app contact paul.freihaut@psychologie.uni-freiburg.de
 */

// React Imports
import React, { Component } from 'react';

// import firebase
import firebase from 'firebase/app';
import 'firebase/auth';
import 'firebase/database';

// Style Imports
import 'bulma/css/bulma.css';
import './App.css';
import 'bulma-extensions/dist/css/bulma-extensions.min.css';

// Import Layout Components (not used in the study)
import Navbar from './LayoutComponents/Navbar';
import Footer from './LayoutComponents/Footer';

// Experimental Page Component Import
import IntroPage from './ExperimentalPages/IntroPage';
import Soziodem from './ExperimentalPages/Soziodem';
import End from "./ExperimentalPages/End";
import BfiNeuroticism from './ExperimentalPages/BfiNeuroticism';
import MentalArithmetic from './ExperimentalPages/MentalArithmetics';
import SamStress from './ExperimentalPages/Sam';
import PointClickTask from './ExperimentalPages/PointClickTask';
import LoadingTask from './ExperimentalPages/LoadingTask';
import DrawingTask from './ExperimentalPages/DrawingTask';
import TrialInstruction from './ExperimentalPages/TrialInstruction';
import TrialEnd from './ExperimentalPages/TrialEnd';
import DragDropTask from './ExperimentalPages/DragDropTask';
import FollowBoxTask from './ExperimentalPages/FollowBoxTask';
import PatternTyping from './ExperimentalPages/PatternTyping';
import Mdbf from './ExperimentalPages/Mdbf';
import QuestionsAfterTasks from './ExperimentalPages/QuestionsAfterTasks';

import EnterUserId from './ExperimentalPages/EnterUserId';

class App extends Component {

  constructor(props) {
      super(props);


      this.proceedPhase = this.proceedPhase.bind(this);
      this.updateScore = this.updateScore.bind(this);
      this.renderComponent = this.renderComponent.bind(this);

      // for debug only - needs to be removed
      // this.goBackPhase = this.goBackPhase.bind(this);
      // this.keypressed = this.keypressed.bind(this);

      // initialize state
      this.state = {
          phase: 0,
          expFlow: false,
          scorePractice: 0,
          scoreHighStress: 0,
          scoreLowStress: 0,
          taskNumLowStress: 0,
          taskNumHighStress: 0,
          uniqueId: true, // in test mode true, in deployment mode null
          physioDataId: null
      }
  }

  // Lifecycle Method Used to Build the order of the experimental pages
  componentWillMount() {

      // draw a random condition: 0 = stress first & 1 = NoStress first
      this.condition = Math.floor(Math.random() * 2);

      // Helper function that shuffles an array from
      // https://stackoverflow.com/questions/2450954/how-to-randomize-shuffle-a-javascript-array?page=1&tab=votes#tab-top
      const shuffleArray = function (array) {
          for (let i = array.length - 1; i > 0; i--) {
              const j = Math.floor(Math.random() * (i + 1));
              [array[i], array[j]] = [array[j], array[i]];
          }
      };

      // Helper function that adds new items (of an array) to another array starting at a specific index
      const insert = (arr, index, newItems) => [
          // part of the array before the specified index
          ...arr.slice(0, index),
          // inserted items
          ...newItems,
          // part of the array after the specified index
          ...arr.slice(index)
      ];

      //store all Mouse and Keyboard Tasks
      this.mouseKeyboardTasks = [
          {phase: "PointClick"},
          {phase: "Drawing"},
          {phase: "DragDrop"},
          {phase: "FollowBox"},
          {phase: "PatternTyping"}
      ];

      // Randomly shuffle the Task Array
      shuffleArray(this.mouseKeyboardTasks);

      // Store all pages of the High Stress Condition
      const highStressCondition = [
          {phase: "HS_Instr"},
          {phase: "HS_LoadingTask"}
      ];

      // Store all pages of the Low Stress Condition
      const lowStressCondition = [
          {phase: "LS_Instr"},
          {phase: "LS_LoadingTask"},
      ];

      // store all paged of the Practice Trial
      const practiceTrial = [
          {phase: "PR_Instruction"},
          {phase: "PR_MentalArithmetic"},
      ];

      // fill the high and low stress condition arrays with trios of a Mental Arithmetic Task, a Mouse or Keyboard Task
      // and a BfiNeuroticism Task
      for (let i=0; i < this.mouseKeyboardTasks.length; i++) {
          // get the name of the phase
          let phaseName = this.mouseKeyboardTasks[i].phase;
          // High Stress Condition
          // push an object trio for each task inside the task array
          highStressCondition.push(
              {phase: "HS_Mental_Arithmetic_" + phaseName},
              {phase: "HS_" + phaseName},
              {phase: "HS_SAM_" + phaseName}
          );
          // do same thing for other condition
          lowStressCondition.push(
              {phase: "LS_Mental_Arithmetic_" + phaseName},
              {phase: "LS_" + phaseName},
              {phase: "LS_SAM_" + phaseName}
          );
          practiceTrial.push(
              {phase: "PR_" + phaseName}
          );
      }

      // Add the Trial EndPage to the End of the Condition Arrays
      highStressCondition.push(
          {phase: "HS_Mdbf"},
          {phase: "HS_End"}
      );
      lowStressCondition.push(
          {phase: "LS_Mdbf"},
          {phase: "LS_End"}
      );
      practiceTrial.push(
          {phase: "PR_End"},
      );

      // Store all default pages (that are not shuffeled and dont depend on the condition
      let startPages = [
          {phase: "UserId"},
          {phase: "Intro"},
          {phase: "Soziodem"},
      ];
      let endPages = [
          {phase: "QuestionsAfterTasks"},
          {phase: "BfiNeuroticism"},
          {phase: "End"}];

      // initialize the Experimental Flow (order of all pages)
      let expFlow;

      // add the start pages to the expFlow
      expFlow = startPages;

      // add the practice pages to the expFlow
      expFlow = insert(expFlow, startPages.length, practiceTrial);

      // add the high- and low-stress trials depending on the condition
      // If the condition is 0 = stress first
      if (this.condition === 0) {
          // add the high stress and then the low stress condition pages to the default pages
          expFlow = insert(expFlow, expFlow.length, highStressCondition);
          expFlow = insert(expFlow, expFlow.length + highStressCondition.length, lowStressCondition);
          // if the condition is 1 = low stress
      } else if (this.condition === 1) {
          // add the low stress and then high stress condition pages to the default pages
          expFlow = insert(expFlow, expFlow.length, lowStressCondition);
          expFlow = insert(expFlow, expFlow.length + lowStressCondition.length, highStressCondition);
      }

      // add the end pages to the experimental Flow
      expFlow = insert(expFlow, expFlow.length, endPages);

      // store the expFlow in the State
      this.setState({expFlow: expFlow});

  }

  componentDidMount() {
    // for debug only, needs to be removed in later versions
    // document.addEventListener('keypress', this.keypressed);
    // prevents accidental closing of the study
    window.onbeforeunload = function () {
      return "Bitte laden Sie die Seite nicht neu, da sonst Ihre Daten verloren gehen."
    };

    // Initialize firebase: Put your firebase project credentials here
    firebase.initializeApp({
      apiKey: "",
      authDomain: "",
      databaseURL: "",
      projectId: "",
      storageBucket: "",
      messagingSenderId: ""
    });

    firebase.auth().onAuthStateChanged(user => {
        if (user) {

          console.log("User started experiment: " + user.uid);

          // set the user id as a state and relevant path to save the data in the database and create a subId from the
          // user id to give the experimentor an Id to write down for data saving (uniqueness not guaranteed but very likely)
          this.setState({
            uniqueId: user.uid,
            physioDataId: user.uid.slice(0, 6) + Math.floor((Math.random() * (999 - 100 + 1) + 100)).toString()
          }, () =>  firebase.database().ref(this.state.uniqueId + "/MetaData").set({
            physioDataId: this.state.physioDataId,
            condition: this.condition,
              taskOrder: this.mouseKeyboardTasks
          }));
        }
    });

    // sign in anonymously and keeping the sign-in information only until the page is refreshed
    firebase.auth().setPersistence(firebase.auth.Auth.Persistence.NONE)
        .then(function () {
          return firebase.auth().signInAnonymously();
        })
        .catch(function (error) {
          let errorCode = error.code;
          let errorMessage = error.message;
          console.log(errorCode, errorMessage)
        })

  }

  // componentWillUnmount() {
  //   // for debug only, needs to be removed in later versions
  //   document.removeEventListener('keypress', this.keypressed);
  //
  // }

  // manually skip through experiment using the k and w key
  // for debugging only, needs to be removed in later versions
  // keypressed(event){
  //   event.key === "q" ? this.proceedPhase() :
  //       event.key === "w" ? this.goBackPhase() : console.log("nothing")
  // }

  // go to the next experimental page and store the collected data in the database
  proceedPhase(path, dataToSave){

    // Log the datapath and data for debugging while database is disabled
    console.log(path, dataToSave);

    // save the timestamp when component finished
     firebase.database().ref(this.state.uniqueId + "/phaseFinishedTimestamps").update({
         [this.state.expFlow[this.state.phase].phase]: Date.now()
     });

     // if the proceedPhase function passes a path and data
     if (path && dataToSave) {
         if (Array.isArray(dataToSave)) {
             // override path in database if data is in an array (tracker data)
             firebase.database().ref(this.state.uniqueId + "/" + path).set(dataToSave);
         } else {
             // update path in database with data if data is not an array --> questionnaire data
             firebase.database().ref(this.state.uniqueId + "/" + path).update(dataToSave);
         }
     }

     // increament the phase counter moving on in the experiment
    this.setState({phase: this.state.phase + 1});
  }

  // For debugging only
  // goBackPhase(){
  //   this.setState({phase: this.state.phase - 1});
  // }

  updateScore(newScore, condition, taskNum) {
    if (condition === "lowStress") {
      this.setState({
        scoreLowStress: newScore,
        taskNumLowStress: taskNum
      });
    } else if (condition === "highStress") {
      this.setState({
        scoreHighStress: newScore,
        taskNumHighStress: taskNum
      });
    }

  }

  renderComponent(phase) {

    const experimentalPages = {
      // General Pages
      "UserId": <EnterUserId userId={this.state.physioDataId} proceedPhase={this.proceedPhase}/>,
      "Intro": <IntroPage proceedPhase={this.proceedPhase}/>,
      "Soziodem": <Soziodem phaseName={this.state.expFlow[phase].phase} proceedPhase={this.proceedPhase}/>,
      "QuestionsAfterTasks": <QuestionsAfterTasks phaseName={this.state.expFlow[phase].phase} proceedPhase={this.proceedPhase}/>,
      "BfiNeuroticism": <BfiNeuroticism phaseName={this.state.expFlow[phase].phase} proceedPhase={this.proceedPhase}/>,
      "End": <End participantId={this.state.physioDataId}/>,
      // Practice Tasks & Questionnaires
      "PR_Instruction": <TrialInstruction condition={"practice"} proceedPhase={this.proceedPhase}/>,
      "PR_MentalArithmetic": <MentalArithmetic phaseName={this.state.expFlow[phase].phase} taskNumber={0} score={0} updateScore={this.updateScore} condition={"practice"} proceedPhase={this.proceedPhase}/>,
      "PR_PointClick": <PointClickTask phaseName={this.state.expFlow[phase].phase} condition={"practice"} proceedPhase={this.proceedPhase}/>,
      "PR_Drawing": <DrawingTask phaseName={this.state.expFlow[phase].phase} condition={"practice"} proceedPhase={this.proceedPhase}/>,
      "PR_DragDrop": <DragDropTask phaseName={this.state.expFlow[phase].phase} condition={"practice"} proceedPhase={this.proceedPhase}/>,
      "PR_FollowBox": <FollowBoxTask phaseName={this.state.expFlow[phase].phase} proceedPhase={this.proceedPhase} condition={"practice"}/>,
      "PR_PatternTyping": <PatternTyping phaseName={this.state.expFlow[phase].phase} condition={"practice"} proceedPhase={this.proceedPhase}/>,
      "PR_End": <TrialEnd condition={"practice"} proceedPhase={this.proceedPhase}/>,
      // High Stress Tasks & Questionnaires
      "HS_Instr": <TrialInstruction order={this.condition} condition={"highStress"} proceedPhase={this.proceedPhase}/>,
      "HS_LoadingTask": <LoadingTask phaseName={this.state.expFlow[phase].phase} proceedPhase={this.proceedPhase}/>,
      "HS_Mental_Arithmetic_PointClick": <MentalArithmetic phaseName={this.state.expFlow[phase].phase} taskNumber={this.state.taskNumHighStress} score={this.state.scoreHighStress} updateScore={this.updateScore} condition={"highStress"} proceedPhase={this.proceedPhase}/>,
      "HS_Mental_Arithmetic_Drawing": <MentalArithmetic phaseName={this.state.expFlow[phase].phase} taskNumber={this.state.taskNumHighStress} score={this.state.scoreHighStress} updateScore={this.updateScore} condition={"highStress"} proceedPhase={this.proceedPhase}/>,
      "HS_Mental_Arithmetic_PatternTyping": <MentalArithmetic phaseName={this.state.expFlow[phase].phase} taskNumber={this.state.taskNumHighStress} score={this.state.scoreHighStress} updateScore={this.updateScore} condition={"highStress"} proceedPhase={this.proceedPhase}/>,
      "HS_Mental_Arithmetic_DragDrop": <MentalArithmetic phaseName={this.state.expFlow[phase].phase} taskNumber={this.state.taskNumHighStress} score={this.state.scoreHighStress} updateScore={this.updateScore} condition={"highStress"} proceedPhase={this.proceedPhase}/>,
      "HS_Mental_Arithmetic_FollowBox": <MentalArithmetic phaseName={this.state.expFlow[phase].phase} taskNumber={this.state.taskNumHighStress} score={this.state.scoreHighStress} updateScore={this.updateScore} condition={"highStress"} proceedPhase={this.proceedPhase}/>,
     "HS_PointClick": <PointClickTask phaseName={this.state.expFlow[phase].phase} condition={"highStress"} proceedPhase={this.proceedPhase}/>,
      "HS_Drawing": <DrawingTask phaseName={this.state.expFlow[phase].phase} condition={"highStress"} proceedPhase={this.proceedPhase}/>,
      "HS_DragDrop": <DragDropTask phaseName={this.state.expFlow[phase].phase} condition={"highStress"} proceedPhase={this.proceedPhase}/>,
      "HS_FollowBox": <FollowBoxTask phaseName={this.state.expFlow[phase].phase} proceedPhase={this.proceedPhase} condition={"highStress"}/>,
      "HS_PatternTyping": <PatternTyping phaseName={this.state.expFlow[phase].phase} condition={"highStress"} proceedPhase={this.proceedPhase}/>,
      "HS_SAM_PointClick": <SamStress phaseName={this.state.expFlow[phase].phase} proceedPhase={this.proceedPhase}/>,
      "HS_SAM_DragDrop": <SamStress phaseName={this.state.expFlow[phase].phase} proceedPhase={this.proceedPhase}/>,
      "HS_SAM_Drawing": <SamStress phaseName={this.state.expFlow[phase].phase} proceedPhase={this.proceedPhase}/>,
      "HS_SAM_FollowBox": <SamStress phaseName={this.state.expFlow[phase].phase} proceedPhase={this.proceedPhase}/>,
      "HS_SAM_PatternTyping": <SamStress phaseName={this.state.expFlow[phase].phase} proceedPhase={this.proceedPhase}/>,
      "HS_Mdbf": <Mdbf phaseName={this.state.expFlow[phase].phase} proceedPhase={this.proceedPhase}/>,
      "HS_End": <TrialEnd condition={"highStress"} proceedPhase={this.proceedPhase}/>,
      // Low Stress Tasks & Questionnaires
      "LS_Instr": <TrialInstruction order={this.condition} condition={"lowStress"} proceedPhase={this.proceedPhase}/>,
      "LS_LoadingTask": <LoadingTask phaseName={this.state.expFlow[phase].phase} proceedPhase={this.proceedPhase}/>,
      "LS_Mental_Arithmetic_PointClick": <MentalArithmetic phaseName={this.state.expFlow[phase].phase} taskNumber={this.state.taskNumLowStress} score={this.state.scoreLowStress} updateScore={this.updateScore} condition={"lowStress"} proceedPhase={this.proceedPhase}/>,
      "LS_Mental_Arithmetic_Drawing": <MentalArithmetic phaseName={this.state.expFlow[phase].phase} taskNumber={this.state.taskNumLowStress} score={this.state.scoreLowStress} updateScore={this.updateScore} condition={"lowStress"} proceedPhase={this.proceedPhase}/>,
      "LS_Mental_Arithmetic_DragDrop": <MentalArithmetic phaseName={this.state.expFlow[phase].phase} taskNumber={this.state.taskNumLowStress} score={this.state.scoreLowStress} updateScore={this.updateScore} condition={"lowStress"} proceedPhase={this.proceedPhase}/>,
      "LS_Mental_Arithmetic_FollowBox": <MentalArithmetic phaseName={this.state.expFlow[phase].phase} taskNumber={this.state.taskNumLowStress} score={this.state.scoreLowStress} updateScore={this.updateScore} condition={"lowStress"} proceedPhase={this.proceedPhase}/>,
      "LS_Mental_Arithmetic_PatternTyping": <MentalArithmetic phaseName={this.state.expFlow[phase].phase} taskNumber={this.state.taskNumLowStress} score={this.state.scoreLowStress} updateScore={this.updateScore} condition={"lowStress"} proceedPhase={this.proceedPhase}/>,
      "LS_PointClick": <PointClickTask phaseName={this.state.expFlow[phase].phase} condition={"lowStress"} proceedPhase={this.proceedPhase}/>,
      "LS_Drawing": <DrawingTask phaseName={this.state.expFlow[phase].phase} condition={"lowStress"} proceedPhase={this.proceedPhase}/>,
      "LS_DragDrop": <DragDropTask phaseName={this.state.expFlow[phase].phase} condition={"lowStress"} proceedPhase={this.proceedPhase}/>,
      "LS_FollowBox": <FollowBoxTask phaseName={this.state.expFlow[phase].phase} proceedPhase={this.proceedPhase} condition={"lowStress"}/>,
      "LS_PatternTyping": <PatternTyping phaseName={this.state.expFlow[phase].phase} condition={"lowStress"} proceedPhase={this.proceedPhase}/>,
      "LS_SAM_PointClick": <SamStress phaseName={this.state.expFlow[phase].phase} proceedPhase={this.proceedPhase}/>,
      "LS_SAM_Drawing": <SamStress phaseName={this.state.expFlow[phase].phase} proceedPhase={this.proceedPhase}/>,
      "LS_SAM_DragDrop": <SamStress phaseName={this.state.expFlow[phase].phase} proceedPhase={this.proceedPhase}/>,
      "LS_SAM_FollowBox": <SamStress phaseName={this.state.expFlow[phase].phase} proceedPhase={this.proceedPhase}/>,
      "LS_SAM_PatternTyping": <SamStress phaseName={this.state.expFlow[phase].phase} proceedPhase={this.proceedPhase}/>,
      "LS_Mdbf": <Mdbf phaseName={this.state.expFlow[phase].phase} proceedPhase={this.proceedPhase}/>,
      "LS_End": <TrialEnd condition={"lowStress"} proceedPhase={this.proceedPhase}/>,
    };

    return (
       experimentalPages[this.state.expFlow[phase].phase]
    )
  }

  // page that is shown if firebase login is not done yet
  renderSigningIn() {
    return (
        <div className="section">
          <div className="content">
            <h1>Bitte warten...</h1>
          </div>
        </div>);
  }

  // render the experimental page
  render() {
    return (
      <div className="outerContainer">

        {/*<Navbar/>*/}

        <div className="innerContainer">
          {!this.state.uniqueId ? this.renderSigningIn() : this.renderComponent(this.state.phase)}
        </div>

        {/*<Footer/>*/}

      </div>
    );
  }
}

export default App;
