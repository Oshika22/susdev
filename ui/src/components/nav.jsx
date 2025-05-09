import { useState, useEffect } from "react";
import { Link } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Navbar, Nav, NavDropdown, Container } from "react-bootstrap";

function BasicNavbar({ scrollToSection, refs }) {
  const [scroll, setScroll] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 50) {
        setScroll(true);
      } else {
        setScroll(false);
      }
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);
  return (
    <Navbar expand="lg" className={`fixed top-0 left-0 w-full z-50 transition-all duration-300 ${
      scroll ? "bg-white shadow-md" : "bg-transparent"}`} style={{ position: "fixed", top: 0, left: 0 }}>
      <Container>
        <Navbar.Brand as={Link} to="/" className="font-semibold font-Limelight mt-2"><h4 className="bg-gradient-to-r from-purple-900 via-purple-700 to-purple-900 text-transparent bg-clip-text">UrbanOptima</h4></Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link onClick={() => scrollToSection(refs.homeRef)}>Home</Nav.Link>
            <Nav.Link onClick={() => scrollToSection(refs.dashRef)}>Dashboard</Nav.Link>
            <Nav.Link onClick={() => scrollToSection(refs.aboutRef)}>About Us</Nav.Link>
            <Nav.Link onClick={() => scrollToSection(refs.teamRef)}>Team</Nav.Link>
            <NavDropdown title="Services" id="basic-nav-dropdown"> 
              <NavDropdown.Item href="#action/3.1">Prediction</NavDropdown.Item>
              <NavDropdown.Item href="#action/3.2">ChatBot</NavDropdown.Item>
              <NavDropdown.Item href="#action/3.3">Results</NavDropdown.Item>
            </NavDropdown>
            <Nav.Link href="#link">Contact Us</Nav.Link>
            <Nav.Link as={Link} to="/signin">Signin</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default BasicNavbar;
