// Intro Page of the entire experiment

import React, { Component } from 'react';

import ProceedButton from '../LayoutComponents/ProceedButton';


export default class IntroPage extends Component {

    constructor(props) {
        super(props);
        this.state = {
            checked: false
        };

        this.toggleCheckBox = this.toggleCheckBox.bind(this);
    }

    componentDidMount() {
        window.scrollTo(0, 0);
    }

    toggleCheckBox() {
        this.state.checked ? this.setState({checked: false}) : this.setState({checked: true})
    }

    render() {
        return(
            <div className="section">
                <div className="content">
                    <h3>Wilkommen! Vielen Dank für Ihre Unterstützung dieser Studie!</h3><br/><br/>
                    <div style={{textAlign: "left"}}>
                        <h5>Bevor es losgeht, hier ein paar einführende Informationen:</h5>
                        <p>In der Studie geht es um die Bearbeitung von verschiedenen Aufgaben. Nachfolgend werden Sie
                            gebeten, eben solche Aufgaben zu bearbeiten und dazu verschiedene Fragen zu beantworten. Die Aufgaben sind
                        in einen Übungsblock und zwei Aufgabenblöcken unterteilt. In einem der beiden Aufgabenblöcke
                        wird dabei Ihre Leistung getestet. Im anderen Aufgabenblock
                        geschieht dies nicht. Ob Ihre Leistung in dem Aufgabenblock getestet wird oder nicht, wird Ihnen
                            vor Beginn des Aufgabenblocks mitgeteilt.</p>
                        <p>Über das, was im Einzelnen zu tun ist, erhalten Sie genaue Anleitungen. Lesen Sie diese bitte
                            aufmerksam durch und bearbeiten Sie die Aufgaben so gut Sie können.</p>
                        <p><strong>Hinweis: </strong>Bitte lassen Sie während der gesamten Dauer
                            der Teilnahme Ihr Browserfenster maximiert und benutzen Sie keinen Zoom. Laden Sie bitte
                            außerdem die Seite nicht neu. Sobald Sie Ihre Angaben mit dem Drücken auf "Weiter" bestätigen,
                            können Sie diese nicht mehr verändern.</p>
                        <p>Sollten Sie während der Bearbeitung Fragen haben, wenden Sie sich bitte an die Versuchsleitung.</p><br/>
                    </div>
                    <label className="checkbox" style={{display: "flex", alignItems: "center", marginTop: "25px"}}>
                        <input type="checkbox" style={{marginRight: "5px"}} checked={this.state.checked} onChange={this.toggleCheckBox}/>
                        Ich habe alle Informationen gelesen und bin bereit, mit der Studie zu beginnen
                    </label>
                    <ProceedButton onClick={() => this.props.proceedPhase()} disabled={!this.state.checked}/>
                </div>
            </div>
        );
    }

}