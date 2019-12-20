// final page of experiment

import React, { Component } from 'react';


export default class End extends Component {

    componentDidMount() {
        window.scrollTo(0, 0);
    }

    render() {
        return(
            <div className="section">
                <div className="content" style={{}}>
                    <h3>Die Studie ist beendet. Vielen Dank für Ihre Teilnahme!</h3><br/><br/>
                    <div style={{textAlign: "left"}}>
                        <h5>Abschließende Informationen</h5>
                        <p>
                            Tatsächlich wurde Ihre Leistung während der Aufgabenblöcke nicht evaluiert und mit Richtwerten
                            verglichen. Diese Ankündigung diente dazu, Sie bei der Aufgabenbearbeitung zu stressen. Dies war notwendig, um die mit der
                            Studie verbundenen Forschungsfragen sinnvoll untersuchen zu können. Ziel der Studie ist es
                            herauszufinden, ob die Nutzung der Computermaus- und Tastatur vom Stresslevel während der
                            Nutzung beeinflusst wird.
                        </p>
                        <p>
                            Falls Sie sich von der Studie noch gestresst fühlen, bleiben Sie gerne noch etwas sitzen und
                            nehmen Sie sich Zeit zum Entspannen.
                        </p>
                        <p>
                            Sollten Sie noch Fragen oder Feedback zu der Studie haben, wenden Sie sich an die Versuchsleitung oder an
                            die unten stehende E-Mail Adresse.
                        </p>
                        <p>
                            <strong>Hinweis: </strong>Bitte lassen Sie diese Seite geöffnet.
                        </p>
                        <p>
                            ID des Durchgangs: {this.props.participantId}
                        </p>
                    </div>
                </div>
            </div>
        );
    }

}