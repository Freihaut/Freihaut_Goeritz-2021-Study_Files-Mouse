// Component that shows sociodemografic questions

import React, { Component } from 'react';

import ProceedButton from '../LayoutComponents/ProceedButton';


// Age, Gender, Education, Computer Fluency, Input Device

const divStyle = {
    marginTop: "40px",
};

const questionTextStyle = {
    textAlign: "left",
    fontWeight: "bold"
};


export default class Soziodem extends Component {

    constructor(props) {
        super(props);
        // set a state for each questionnaire item
        this.state = {
            socioDemographics: {
                age: -99,
                sex: -99,
                occupation: -99,
                hand: -99,
            }
        };

        this.handleInputChange = this.handleInputChange.bind(this);
        this.isQuestionnaireComplete = this.isQuestionnaireComplete.bind(this);
    }

    componentDidMount() {
        window.scrollTo(0, 0)
    };

    isQuestionnaireComplete() {
        // check if all questions have a value other than -99 --> each question is answered, if yes, enable proceedphase button
        for (let property in this.state.socioDemographics) {
            if (this.state.socioDemographics.hasOwnProperty(property)) {
                //console.log(property + " = " + this.state[property]);
                if (this.state.socioDemographics[property] === -99) {
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

        let socioDemographics = {...this.state.socioDemographics};
        socioDemographics[name] = parseInt(value);
        this.setState({socioDemographics});
    }

    render() {

        return(
            <div className="section">
            <div className="content">
                <div>
                    <h4>Machen Sie zunächst bitte einige Angaben zu Ihrer Person</h4>
                    <hr style={{margin: "0 0", height: "3px"}}/>
                </div>
                <div className="field" style={{marginTop: "25px"}}>
                    <p style={questionTextStyle}>Ihr Alter in Jahren:</p>
                    <div className="control">
                        <label>
                            <input
                                style={{width: "150px"}}
                                name="age"
                                className="input"
                                type="text"
                                placeholder="Ihr Alter"
                                onChange={this.handleInputChange}
                            />
                            <p style={
                                {color: "hsl(348, 100%, 61%)",
                                    fontSize: "14px",
                                    visibility: isNaN(this.state.socioDemographics.age) ? "visible" : "hidden"
                                }}>Eingabe ungültig, bitte eine Zahl eintragen
                            </p>
                        </label>
                    </div>
                </div>

                <div className="field" style={{marginTop: "26px"}}>
                    <span>
                        <p style={questionTextStyle}>Ihr Geschlecht:</p>
                        <div className="control">
                            <label className="radio">
                                <input
                                    style={{marginRight: 5}}
                                    type="radio"
                                    value="0"
                                    name="sex"
                                    onChange={this.handleInputChange}
                                />Weiblich
                            </label>
                            <label className="radio" style={{marginLeft: 25}}>
                                <input
                                    style={{marginRight: 5}}
                                    type="radio"
                                    value="1"
                                    name="sex"
                                    onChange={this.handleInputChange}
                                />Männlich
                            </label>
                            <label className="radio" style={{marginLeft: 25}}>
                                <input style={{marginRight: 5}}
                                       type="radio"
                                       value="2"
                                       name="sex"
                                       onChange={this.handleInputChange}
                                />Divers
                            </label>
                        </div>
                    </span>
                </div>

                <div className="field" style={divStyle}>
                    <span>
                        <p style={questionTextStyle}>Ihr beruflicher Status:</p>
                        <div className="control">
                            <label className="radio">
                                <input
                                    style={{marginRight: 5}}
                                    type="radio"
                                    value="0"
                                    name="occupation"
                                    onChange={this.handleInputChange}
                                />In der Schule
                            </label>
                            <label className="radio" style={{marginLeft: 25}}>
                                <input
                                    style={{marginRight: 5}}
                                    type="radio"
                                    value="1"
                                    name="occupation"
                                    onChange={this.handleInputChange}
                                />In Ausbildung
                            </label>
                            <label className="radio" style={{marginLeft: 25}}>
                                <input
                                    style={{marginRight: 5}}
                                    type="radio"
                                    value="2"
                                    name="occupation"
                                    onChange={this.handleInputChange}
                                />Im Studium
                            </label>
                            <label className="radio" style={{marginLeft: 25}}>
                                <input style={{marginRight: 5}}
                                       type="radio"
                                       value="3"
                                       name="occupation"
                                       onChange={this.handleInputChange}
                                />Berufstätig
                            </label>
                            <label className="radio" style={{marginLeft: 25}}>
                                <input style={{marginRight: 5}}
                                       type="radio"
                                       value="4"
                                       name="occupation"
                                       onChange={this.handleInputChange}
                                />Sonstiges (z.B. in Rente)
                            </label>
                        </div>
                    </span>
                </div>

                <div className="field" style={divStyle}>
                    <span>
                        <p style={questionTextStyle}>Ihre dominante Hand:</p>
                        <div className="control">
                            <label className="radio">
                                <input
                                    style={{marginRight: 5}}
                                    type="radio"
                                    name="hand"
                                    value="0"
                                    onChange={this.handleInputChange}
                                />Rechtshänder
                            </label>
                            <label className="radio" style={{marginLeft: 25}}>
                                <input
                                    style={{marginRight: 5}}
                                    type="radio"
                                    name="hand"
                                    value="1"
                                    onChange={this.handleInputChange}
                                />Linkshänder
                            </label>
                        </div>
                    </span>
                </div>

                <ProceedButton onClick={() => this.props.proceedPhase(this.props.phaseName, this.state.socioDemographics)} disabled={!this.isQuestionnaireComplete()}/>
            </div>
            </div>
        );
    }

}