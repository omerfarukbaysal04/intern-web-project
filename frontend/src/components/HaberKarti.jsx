import { Link } from "react-router-dom"

// Haber karti. Ana sayfa ve kategori sayfasi ayni kalibi kullansin diye
// ayri bir bilesen; onceden ikisi de kendi kopyasini tasiyacakti.
function HaberKarti({ post }) {
  return (
    <Link to={`/post/${post.slug}`} className="card">
      {/* Gorsel varsa kapak olarak basilir; yoksa kategori rengi (tone) kalir. */}
      <div className={`thumb ${post.tone}`}>
        {post.gorsel && (
          <img src={post.gorsel.dosya} alt={post.gorsel.alt} loading="lazy" />
        )}
        <span className="chip">{post.category}</span>
      </div>
      <div className="cbody">
        <h3>{post.title}</h3>
        <p>{post.excerpt}</p>
        <div className="meta">
          <span>{post.author}</span>
          <span>·</span>
          <span className="mono">{post.date}</span>
          <span>·</span>
          <span className="mono">{post.read_minutes} dk</span>
        </div>
      </div>
    </Link>
  )
}

export default HaberKarti
