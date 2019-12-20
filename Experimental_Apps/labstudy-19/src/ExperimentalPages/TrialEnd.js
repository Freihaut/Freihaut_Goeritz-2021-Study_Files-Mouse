// end page of the trials

import React, {Component} from 'react';
import '../StyleSheets/resultsLoader.css';

import ProceedButton from '../LayoutComponents/ProceedButton';

export default class TrialEnd extends Component {

    constructor(props) {
        super(props);
        this.state = {
            loaded: false
        };

    }

    componentDidMount() {
        window.scrollTo(0, 0);

        this.timer = setTimeout(
            () => this.setState({loaded: true}),
            7500
        )
    }

    componentWillUnmount() {
        clearTimeout(this.timer)
    }


    renderOutroText(props) {
        // Practice Condition
        if (props === "practice") {
            return(
                <div className="content">
                    <h3>Der Übungsblock ist beendet.</h3><br/>
                    <h4>Im weiteren Verlauf der Studie beginnen die Aufgaben sofort ohne einleitende Erklärung.</h4>
                    <h4>Falls jetzt noch Unklarheiten oder Fragen bestehen, wenden Sie sich unmittelbar an die Versuchsleitung.</h4><br/>
                    <h4>Drücken Sie auf "Weiter" um fortzufahren.</h4>
                    <ProceedButton onClick={() => this.props.proceedPhase()}/>
                </div>
            )
            // Low Stress Condition
        } else if (props === "lowStress") {
            return(
                <div className="content">
                    <h2>Der Aufgabenblock ist beendet.</h2><br/>
                    <h4>Drücken Sie auf "Weiter" um fortzufahren.</h4>
                    <ProceedButton onClick={() => this.props.proceedPhase()}/>
                </div>
            )
            // High Stress Condition
        }  else if(props === "highStress") {
            if (!this.state.loaded) {
                return(
                    <div className="content">
                        <h3>Bitte warten Sie kurz, während Ihre Leistung ausgewertet wird.</h3><br/>
                        <div style={{display: "flex",
                            alignItems: "center",
                            flexDirection: "column",
                            justifyContent: "center",}}>
                            <div className="lds-ellipsis">
                                <div></div>
                                <div></div>
                                <div></div>
                                <div></div>
                            </div>
                        </div>
                    </div>
                )
            } else {
                return(
                    <div className="content">
                        <h2>Der Aufgabenblock ist beendet.</h2><br/>
                        <h4>Sie haben das festgelegte Leistungsmaß erfüllt. Es ist keine weitere Prüfung Ihrer Fähigkeiten
                            notwendig.</h4>
                        <h4>Drücken Sie auf "Weiter" um fortzufahren.</h4>
                        <ProceedButton onClick={() => this.props.proceedPhase()}/>
                    </div>
                        )
            }
        }
    }

    render() {
        return (
            <div className="section">
                {this.renderOutroText(this.props.condition)}
            </div>
        );
    }

}