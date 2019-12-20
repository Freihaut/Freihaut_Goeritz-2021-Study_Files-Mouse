// Component that shows the BFI neuroticism questionnaire used in the study


import React, {Component} from 'react';

import MatrixQuestion from '../LayoutComponents/MatrixQuestion';
import MatrixButtons from '../LayoutComponents/MatrixButton';
import ProceedButton from '../LayoutComponents/ProceedButton';

const scaleQuestions = [
    {question: "Ich bleibe auch in stressigen Situationen gelassen.", id: 'NE1R'},
    {question: "Ich bleibe auch bei Rückschlägen zuversichtlich.", id: 'NE2R'},
    {question: "Ich kann launisch sein, habe schwankende Stimmungen.", id: 'NE3'},
    {question: "Ich reagiere leicht angespannt.", id: 'NE4'},
    {question: "Ich bin selbstsicher, mit mir zufrieden.", id: 'NE5R'},
    {question: "Ich bin ausgeglichen, nicht leicht aus der Ruhe\n" +
            "zu bringen.", id: 'NE6R'},
    {question: "Ich mache mir oft Sorgen.", id: 'NE7'},
    {question: "Ich fühle mich oft bedrückt, freudlos.", id: 'NE8'},
    {question: "Ich habe meine Gefühle unter Kontrolle, werde\n" +
            "selten wütend.", id: 'NE9R'},
    {question: "Ich werde selten nervös und unsicher.", id: 'NE10R'},
    {question: "Ich bin oft deprimiert, niedergeschlagen.", id: 'NE11'},
    {question: "Ich reagiere schnell gereizt oder genervt.", id: 'NE12'},
];

const scaleAnchors = [
    {anchor: ""},
    {anchor: "sehr unzutreffend"},
    {anchor: "eher unzutreffend"},
    {anchor: "weder noch"},
    {anchor: "eher zutreffend"},
    {anchor: "sehr zutreffend"},
];


export default class BfiNeuroticism extends Component {

    constructor(props) {
        super(props);

        // set each intitial questionnaire value to -99 and save them as a state
        let initialMdbf = {};
        scaleQuestions.forEach(item => {
            initialMdbf[item.id] = -99;
        });

        this.state = {MDBF: initialMdbf};

        this.handleInputChange = this.handleInputChange.bind(this);
        this.isQuestionnaireComplete = this.isQuestionnaireComplete.bind(this);
    }

    componentDidMount() {
        window.scrollTo(0, 0);
    }

    isQuestionnaireComplete() {
        // check if all questions have a value other than -99 --> each question is answered, if yes, enable proceedphase button
        for (let property in this.state.MDBF) {
            if (this.state.MDBF.hasOwnProperty(property)) {
                //console.log(property + " = " + this.state[property]);
                if (this.state.MDBF[property] === -99) {
                    return false;
                }
            }
        }

        return true;
    }

    handleInputChange(event) {
        // Get the name and value of the clicked radio button and save it to the corresponding question state
        const target = event.target;
        const value = target.value;
        const name = target.name;

        let MDBF = {...this.state.MDBF};
        MDBF[name] = parseInt(value);
        this.setState({MDBF});
    }

    render() {
        return (
            <div className="section">
                <div className="content" style={{}}>
                    <div>
                        <h4>Bitte geben Sie für jede der folgenden Aussagen an, inwieweit Sie zustimmen.</h4>
                        <hr style={{margin: "0 0", height: "3px"}}/>
                    </div>
                    <div style={{marginTop: "40px"}}>
                        <table className="table is-hoverable">
                            <tbody>
                            <tr>
                                {scaleAnchors.map((tags, index) => (
                                    <th style={{textAlign: "center"}} key={index}>{tags.anchor}</th>
                                ))}
                            </tr>
                            {scaleQuestions.map(question => (
                                <tr key={question.question}>
                                    <MatrixQuestion question={question.question}/>
                                    {scaleAnchors.slice(1).map((tags, index) => (
                                        <MatrixButtons
                                            key={index}
                                            name={question.id}
                                            value={index}
                                            onChange={this.handleInputChange}
                                        />
                                    ))}
                                </tr>
                            ))
                            }
                            </tbody>
                        </table>
                    </div>
                    <ProceedButton disabled={!this.isQuestionnaireComplete()}
                                   onClick={() => this.props.proceedPhase(this.props.phaseName, this.state.MDBF)}/>
                </div>
            </div>
        );
    }

}