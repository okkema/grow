import LineChart from "./charts/LineChart"
import { useSensorStream, useSensorHistory } from "./sensors"

function App() {
  const { history, current } = useSensorStream()
  const raw = JSON.stringify(current, null, "\t")
  const temperature = history.map(x => ({ x: new Date(x.timestamp), y: x.data.temperature }))
  const humidity = history.map(x => ({ x: new Date(x.timestamp), y: x.data.humidity }))
  const { data } = useSensorHistory()
  const test = data.map(x => ({ x: new Date(x.timestamp), y: x.temperature }))
  return (
    <div>
      <pre>{raw}</pre>
      {!!history.length && <LineChart data={temperature} />}
      {!!history.length && <LineChart data={humidity} color="blue" />}
      {!!data.length && <LineChart data={test} color="green" />}
    </div>
  )
}

export default App
