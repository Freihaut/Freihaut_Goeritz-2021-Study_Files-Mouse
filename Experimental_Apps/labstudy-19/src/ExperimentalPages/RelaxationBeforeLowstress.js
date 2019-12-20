// not used in the final experimental app
// shows an image and asks participants to relax for a certain ammount of time
// rational of component was to give participants some rest before the start of the low-stress condition

import React, {Component} from 'react';

import RelaxGif from '../Images/Relax12.gif';
import Gong from '../Sounds/Gong.mp3';

export default class RelaxationBeforeLowstress extends Component {

    componentDidMount() {
        window.scrollTo(0, 0);

        const taskEnd = 65000;

        this.gong = setTimeout(() =>{
            let sound = new Audio(Gong);
            sound.play();
        }, taskEnd - 5000);

        this.timer = setTimeout( () => {
            this.props.proceedPhase();
            }, taskEnd
        )
    }

    componentWillUnmount() {
        clearTimeout(this.timer);
        clearTimeout(this.gong);
    }

    render() {
        return (
            <div className="section">
                <div className="content" style={{}}>
                    <h3>Zeit zum Durchatmen</h3>
                    <h5>
                        Bevor der nächsten Aufgabenblock beginnt, können Sie kurz Zeit zum Durchatmen.
                    </h5>
                    <h5>
                        Für viele Menschen gelingt dies zum Beispiel gut durch langsames und regelmäßiges Ein-und Ausatmen.
                        Gerne können Sie dabei die Augen schließen oder das Bild betrachten.
                    </h5>
                    <h5>Nach etwa 1 Minute hören Sie einen Gong und werden anschließend automatisch zur nächsten Seite weitergeleitet.</h5><br/><br/>
                    <div style={{display: "flex", justifyContent: "center"}}>
                        <figure style={{}}>
                            <img alt="loading_failed" src={RelaxGif} />
                        </figure>
                    </div>
                </div>
            </div>
        );
    }

}