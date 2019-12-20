// first page of experiment in which a unique anonymous user id is shown to be able to assign the data collected in
// this experimental app to the physiological data collected in the experiment (independent of this app)

import React from 'react';
import ProceedButton from "../LayoutComponents/ProceedButton";

export default function Login (props) {

    return (
        <section className="section">
            <div className="content">
                <p className="title is-3">
                    Versuchspersonen ID
                </p>
                <p className="subtitle is-5">
                    zur Zuordnung der Studiendaten mit den physiologischen Daten:
                </p>
                <h1>
                    {props.userId}
                </h1>
            </div>
            <ProceedButton onClick={() => props.proceedPhase()}/>
        </section>
    );
}