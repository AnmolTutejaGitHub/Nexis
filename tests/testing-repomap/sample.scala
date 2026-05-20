import scala.collection.mutable.{Map, ArrayBuffer}

case class Record(id: Int, name: String, tags: List[String] = Nil)

trait Searchable[T] {
  def findById(id: Int): Option[T]
  def findAll(): List[T]
}

class Repository extends Searchable[Record] {
  private val store: Map[Int, Record] = Map()

  def findById(id: Int): Option[Record] = store.get(id)
  def findAll(): List[Record] = store.values.toList
  def save(record: Record): Unit = store.put(record.id, record)
  def delete(id: Int): Boolean = store.remove(id).isDefined
}

object Utils {
  def formatRecord(r: Record): String = s"[${r.id}] ${r.name}"

  def groupByTag(records: List[Record]): Map[String, ArrayBuffer[Record]] = {
    val result: Map[String, ArrayBuffer[Record]] = Map()
    for (r <- records; tag <- r.tags)
      result.getOrElseUpdate(tag, ArrayBuffer()) += r
    result
  }
}

def processRecords(records: List[Record]): List[String] =
  records.map(r => Utils.formatRecord(r))
