import QtQuick

Rectangle {
    id: root
    color: "black"

    property string currentTime: ""
    property string currentDate: ""

    property int frameIndex: 0

    property var frames: [
        "qrc:/assets/frames/frame01.png",
        "qrc:/assets/frames/frame02.png",
        "qrc:/assets/frames/frame03.png",
        "qrc:/assets/frames/frame04.png",
        "qrc:/assets/frames/frame05.png",
        "qrc:/assets/frames/frame06.png",
        "qrc:/assets/frames/frame07.png",
        "qrc:/assets/frames/frame08.png",
        "qrc:/assets/frames/frame09.png",
        "qrc:/assets/frames/frame10.png"
    ]

    FontLoader {
        id: pixelFont
        source: fontSource
    }

    Image {
        id: bg
        anchors.fill: parent
        source: frames[frameIndex]
        fillMode: Image.PreserveAspectCrop
    }

    Timer {
        interval: 500
        running: true
        repeat: true

        onTriggered: {
            frameIndex = (frameIndex + 1) % frames.length
        }
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
                "Sunday","Monday","Tuesday","Wednesday",
                "Thursday","Friday","Saturday"
            ]
            const months = [
                "January","February","March","April",
                "May","June","July","August",
                "September","October","November","December"
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

        property real lastX: -1
        property real lastY: -1
        property real threshold: 12

        onClicked: Qt.quit()

        onPositionChanged: function(mouse) {
            if (lastX < 0 || lastY < 0) {
                lastX = mouse.x
                lastY = mouse.y
                return
            }

            const dx = mouse.x - lastX
            const dy = mouse.y - lastY

            if (dx * dx + dy * dy >= threshold * threshold) {
                Qt.quit()
                return
            }

            lastX = mouse.x
            lastY = mouse.y
        }
    }

    focus: true

    Keys.onPressed: function(event) {
        event.accepted = true
        Qt.quit()
    }
}