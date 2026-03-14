import QtQuick
import QtMultimedia

Rectangle {
    id: root
    color: "black"

    property string currentTime: ""
    property string currentDate: ""

    FontLoader {
        id: pixelFont
        source: fontSource
    }

    Video {
        id: bgVideo
        anchors.fill: parent
        source: videoSource
        autoPlay: true
        loops: MediaPlayer.Infinite
        muted: true
        fillMode: VideoOutput.PreserveAspectCrop
    }

    Column {
        anchors.horizontalCenter: parent.horizontalCenter
        y: parent.height * 0.58
        spacing: 14

        Text {
            text: root.currentTime
            anchors.horizontalCenter: parent.horizontalCenter
            color: "white"
            font.family: pixelFont.status === FontLoader.Ready ? pixelFont.name : "monospace"
            font.pixelSize: 64
            horizontalAlignment: Text.AlignHCenter
            style: Text.Outline
            styleColor: "#000000"
        }

        Text {
            text: root.currentDate
            anchors.horizontalCenter: parent.horizontalCenter
            color: "white"
            font.family: pixelFont.status === FontLoader.Ready ? pixelFont.name : "monospace"
            font.pixelSize: 28
            horizontalAlignment: Text.AlignHCenter
            style: Text.Outline
            styleColor: "#000000"
        }
    }

    Timer {
        interval: 1000
        running: true
        repeat: true

        function pad(n) {
            return n < 10 ? "0" + n : "" + n
        }

        function englishDate(d) {
            const weekdays = [
                "Sunday", "Monday", "Tuesday", "Wednesday",
                "Thursday", "Friday", "Saturday"
            ]
            const months = [
                "January", "February", "March", "April",
                "May", "June", "July", "August",
                "September", "October", "November", "December"
            ]

            return weekdays[d.getDay()] + ", "
                + months[d.getMonth()] + " "
                + d.getDate() + ", "
                + d.getFullYear()
        }

        function updateDateTime() {
            const now = new Date()
            root.currentTime = pad(now.getHours()) + ":" + pad(now.getMinutes())
            root.currentDate = englishDate(now)
        }

        onTriggered: updateDateTime()
        Component.onCompleted: updateDateTime()
    }

    MouseArea {
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: Qt.BlankCursor
        onClicked: Qt.quit()
        onPositionChanged: Qt.quit()
    }

    focus: true
    Keys.onPressed: (event) => {
        Qt.quit()
    }
}