#!/usr/bin/env python3

import logging
import requests
from configuration import configuration

# Set up logging
logging.basicConfig()


class BMRBDepSession:
    """ A class to manage the session. """

    sid = None
    session = None
    nmrstar_file = None
    user_email = None

    file_types = {
        "upload_category_1": "Assigned NMR chemical shifts",
        "upload_category_2": "Scalar coupling constants",
        "upload_category_3": "Auto relaxation parameters",
        "upload_category_4": "Tensor data",
        "upload_category_5": "Interatomic distance data",
        "upload_category_6": "Chemical shift anisotropy",
        "upload_category_7": "Heteronuclear NOEs",
        "upload_category_8": "T1 (R1) NMR relaxation data",
        "upload_category_9": "T2 (R2) NMR relaxation data",
        "upload_category_10": "T1rho (R1rho) NMR relaxation data",
        "upload_category_11": "Order parameters",
        "upload_category_12": "Dynamics trajectory file",
        "upload_category_13": "Dynamics movie file",
        "upload_category_14": "Residual dipolar couplings",
        "upload_category_15": "Hydrogen exchange rates",
        "upload_category_16": "Hydrogen exchange protection data",
        "upload_category_17": "Chemical rate constants",
        "upload_category_18": "Spectral peak lists",
        "upload_category_19": "Dipole-dipole couplings",
        "upload_category_20": "Quadrupolar couplings",
        "upload_category_21": "Homonuclear NOEs",
        "upload_category_22": "Dipole-dipole relaxation data",
        "upload_category_23": "Dipole-dipole cross correlation data",
        "upload_category_24": "Dipole-CSA cross correlation data",
        "upload_category_25": "Binding constants",
        "upload_category_26": "NMR-derived pH transitions (pKa's; pHmid's)",
        "upload_category_27": "NMR-derived D/H fractionation factors",
        "upload_category_28": "Theoretical (calculated) chemical shift values",
        "upload_category_29": "Theoretical coupling constants",
        "upload_category_30": "Theoretical heteronuclear NOEs",
        "upload_category_31": "Theoretical T1 values",
        "upload_category_32": "Theoretical T2 values",
        "upload_category_33": "Spectral density factors",
        "upload_category_34": "Time-domain data (raw spectral data)",
        "upload_category_35": "Molecular orientations",
        "upload_category_36": "Secondary structure features",
        "upload_category_37": "Atomic coordinates",
        "upload_category_38": "Mass spectrometry data",
        "upload_category_39": "Other kinds of data",
        "Image": "An image"
    }

    def __init__(self, nmrstar_file, user_email, sid=None):
        if sid:
            self.sid = sid
        else:
            self.nmrstar_file = nmrstar_file
            self.user_email = user_email

    def __enter__(self):
        """ Start the session.

        Creates a python requests Session() and starts an BMRBDep session."""
        self.session = requests.Session()

        # Don't create a new session if we already have a SID
        if self.sid:
            return

        logging.info("Creating session.")
        r = self.session.post("%s/deposition/new" % configuration['bmrb_api'],
                              data={'email': self.user_email},
                              files={'nmrstar_file': ('m2mtool_generated.str', self.nmrstar_file)})
        # If there was an error closing the session raise it
        r.raise_for_status()

        # Find the session ID
        self.sid = r.json()['deposition_id']
        logging.info("Session ID: %s" % self.sid)

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """ End the current session."""

        # End the HTTP session
        self.session.close()

    def upload_file(self, file_name):
        """ Uploads a given file to the session.

        the_file should be a (filename, type) tuple. """

        url = '%s/deposition/%s/file' % (configuration['bmrb_api'], self.sid)
        files = {'file': open(file_name, 'rb')}

        logging.info("Sending file '%s'.", file_name)
        r = self.session.post(url, files=files)
        r.raise_for_status()

    @property
    def session_url(self):
        """ Returns the session URL."""

        return "%s/entry/%s/saveframe/deposited_data_files/category" % \
               (configuration['bmrbdep_url'], self.sid)

