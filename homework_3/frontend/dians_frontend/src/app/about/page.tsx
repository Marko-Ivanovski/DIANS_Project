import Image from "next/image";

const About = () => {
  return (
    <>
      <main>
        {/* First Row */}
        <section className="about-section">
          <div className="row">
            <div className="text-container">
              <div className="badge">Our Mission</div>
              <h2>Who We Are</h2>
              <p>
                At the Macedonian Stock Exchange, we are committed to fostering transparency, growth, and accessibility in the financial market. Established with a vision to empower investors and companies alike, we serve as a bridge connecting opportunities with ambition. Our platform offers real-time market data, a seamless trading experience, and tools designed to help you make informed financial decisions.
              </p>
            </div>
            <div className="image-container">
              <Image src="/Images/WhoWeAre.png" alt="Who We Are" width={500} height={300} />
            </div>
          </div>
        </section>

        {/* Second Row */}
        <section className="about-section">
          <div className="row">
            <div className="image-container">
              <Image src="/Images/Legal.png" alt="Legal" width={500} height={300} />
            </div>
            <div className="text-container">
              <div className="badge">Legal</div>
              <h2>Terms and Conditions</h2>
              <p>
                By using our platform, you agree to abide by our terms and conditions to ensure a secure and fair trading environment for all users. Transactions are subject to regulatory oversight, and users are responsible for the accuracy of the information provided during trades. Unauthorized activities or violations of our policies may result in account suspension. For a detailed overview, refer to our full Terms and Conditions.
              </p>
            </div>
          </div>
        </section>
      </main>
      <br/>
      <br/>
      <br/>
      <br/>
      <br/>
    </>
  );
};

export default About;