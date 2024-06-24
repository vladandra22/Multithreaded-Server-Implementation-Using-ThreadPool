from app import webserver
from flask import request, jsonify
import json
import os

# Example endpoint definition
@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    webserver.logger.info('Start /api/post_endpoint')
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        print(f"got data in post {data}")
        webserver.logger.info(f"Received data in /api/post_endpoint: {data}")

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        webserver.logger.info('End /api/post_endpoint')
        return jsonify(response)
    # Else, Method Not Allowed
    webserver.logger.exception("Method not allowed in /api/post_endpoint")
    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    if request.method == 'GET':
        print(f"JobID is {job_id}")
        webserver.logger.info(f'Start /api/get_results/{job_id}')
        # Check if job_id is valid

        job_id_number = int(job_id[7:])
        job_status = webserver.tasks_runner.get_job_status(int(job_id_number))

        # Avem nevoie sa decrementam counter-ul cu 1, deoarece l-am marit la ultimul
        # request de tip POST.

        curr_job_id = webserver.job_counter - 1

        # Daca job_id-ul nu este inregistrat in dictionar sau nu este intre 1 si
        # job_counter, atunci acesta nu este valid.
        if not job_status or not (int(job_id_number) > 0 and int(job_id_number) <= curr_job_id):
            webserver.logger.exception(f"Invalid job_id in /api/get_results/{job_id}")
            return jsonify({
                'status': "error",
                'reason': "Invalid job_id"
            })

        # Check if job_id is done and return the result
        #    res = res_for(job_id)
        #    return jsonify({
        #        'status': 'done',
        #        'data': res
        #    })

        if job_status['status'] == 'done':
            job_status = webserver.tasks_runner.get_job_status(curr_job_id)
            if not os.path.exists('results'):
                os.makedirs('results')
            with open(f"results/job_id_{job_id_number}.json", 'r', encoding='utf-8') as file:
                result_data = json.load(file)
            res_dict = {
                'status': 'done',
                'data': result_data
            }
            webserver.logger.info(f'End /api/get_results/{job_id} with {res_dict}')
            return jsonify(res_dict)
        # If not, return running status
        return jsonify({'status': 'running'})
    # Else, Method Not Allowed
    webserver.logger.exception(f"Method not allowed in /api/get_results/{job_id}")
    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    if request.method == 'POST':
        # Get request data
        data = request.json
        webserver.logger.info(
            f'Start /api/states_mean with job_id {webserver.job_counter} and data {data}')
        print(f"Got request {data}")

        if webserver.tasks_runner.shutdown_event.is_set():
            return jsonify({"job_id": "job_id_" + str(-1), "reason": "shutting down"})

        question = data.get('question')

        # Register job. Don't wait for task to finish
        task = (webserver.job_counter, webserver.data_ingestor.calculate_states_mean, (question, ))
        webserver.tasks_runner.submit_task(task)

        # Increment job_id counter
        with webserver.job_id_lock:
            current_job_id = webserver.job_counter
            webserver.job_counter += 1

        # Return associated job_id
        webserver.logger.info('End /api/states_mean')
        return jsonify({"job_id": "job_id_" + str(current_job_id)})
    # Else, Method Not Allowed
    webserver.logger.exception("Method not allowed in /api/states_mean")
    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    if request.method == 'POST':
        # Get request data
        data = request.json
        print(f"Got request {data}")
        webserver.logger.info(
            f'Start /api/state_mean with job_id {webserver.job_counter} and data {data}')

        if webserver.tasks_runner.shutdown_event.is_set():
            return jsonify({"job_id": "job_id_" + str(-1), "reason": "shutting down"})

        question = data.get('question')
        state = data.get('state')

        # Register job. Don't wait for task to finish
        task = (webserver.job_counter, webserver.data_ingestor.calculate_state_mean,
                (state, question, ))
        webserver.tasks_runner.submit_task(task)

        # Increment job_id counter
        with webserver.job_id_lock:
            current_job_id = webserver.job_counter
            webserver.job_counter += 1

        webserver.logger.info('End /api/state_mean')
        return jsonify({"job_id": "job_id_" + str(current_job_id)})
    # Else, Method Not Allowed
    webserver.logger.exception("Method not allowed in /api/state_mean")
    return jsonify({"error": "Method not allowed"}), 405


@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    if request.method == 'POST':
        # Get request data
        data = request.json
        print(f"Got request {data}")
        webserver.logger.info(
            f'Start /api/best5 with job_id {webserver.job_counter} and data {data}')

        if webserver.tasks_runner.shutdown_event.is_set():
            return jsonify({"job_id": "job_id_" + str(-1), "reason": "shutting down"})

        question = data.get('question')

        # Register job. Don't wait for task to finish
        task = (webserver.job_counter, webserver.data_ingestor.calculate_best5_states, (question, ))
        webserver.tasks_runner.submit_task(task)

        # Increment job_id counter
        with webserver.job_id_lock:
            current_job_id = webserver.job_counter
            webserver.job_counter += 1

        # Return associated job_id
        webserver.logger.info('End /api/best5')
        return jsonify({"job_id": "job_id_" + str(current_job_id)})
    # Else, Method Not Allowed
    webserver.logger.exception("Method not allowed in /api/best5")
    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    if request.method == 'POST':
        # Get request data
        data = request.json
        print(f"Got request {data}")
        webserver.logger.info(
            f'Start /api/worst5 with job_id {webserver.job_counter} and data {data}')

        if webserver.tasks_runner.shutdown_event.is_set():
            return jsonify({"job_id": "job_id_" + str(-1), "reason": "shutting down"})

        question = data.get('question')

        # Register job. Don't wait for task to finish
        task = (webserver.job_counter, webserver.data_ingestor.calculate_worst5_states,
                (question, ))
        webserver.tasks_runner.submit_task(task)

        # Increment job_id counter
        with webserver.job_id_lock:
            current_job_id = webserver.job_counter
            webserver.job_counter += 1

        # Return associated job_id
        webserver.logger.info('End /api/worst5')
        return jsonify({"job_id": "job_id_" + str(current_job_id)})
    # Else, Method Not Allowed
    webserver.logger.exception("Method not allowed in /api/worst5")
    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    if request.method == 'POST':
        # Get request data
        data = request.json
        print(f"Got request {data}")
        webserver.logger.info(
            f'Start /api/global_mean with job_id {webserver.job_counter} and data {data}')

        if webserver.tasks_runner.shutdown_event.is_set():
            return jsonify({"job_id": "job_id_" + str(-1), "reason": "shutting down"})

        question = data.get('question')

        # Register job. Don't wait for task to finish
        task = (webserver.job_counter, webserver.data_ingestor.calculate_global_mean,
                (question, ))
        webserver.tasks_runner.submit_task(task)

        # Increment job_id counter
        with webserver.job_id_lock:
            current_job_id = webserver.job_counter
            webserver.job_counter += 1

        # Return associated job_id
        webserver.logger.info('End /api/global_mean')
        return jsonify({"job_id": "job_id_" + str(current_job_id)})
    # Else, Method Not Allowed
    webserver.logger.exception("Method not allowed in /api/global_mean")
    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    if request.method == 'POST':
        # Get request data
        data = request.json
        print(f"Got request {data}")
        webserver.logger.info(
            f'Start /api/diff_from_mean with job_id {webserver.job_counter} and data {data}')

        if webserver.tasks_runner.shutdown_event.is_set():
            return jsonify({"job_id": "job_id_" + str(-1), "reason": "shutting down"})

        question = data.get('question')

        # Register job. Don't wait for task to finish
        task = (webserver.job_counter, webserver.data_ingestor.calculate_diff_from_mean,
                (question, ))
        webserver.tasks_runner.submit_task(task)

        # Increment job_id counter
        with webserver.job_id_lock:
            current_job_id = webserver.job_counter
            webserver.job_counter += 1

        # Return associated job_id
        webserver.logger.info('End /api/diff_from_mean')
        return jsonify({"job_id": "job_id_" + str(current_job_id)})
    # Else, Method Not Allowed
    webserver.logger.exception("Method not allowed in /api/diff_from_mean")
    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    if request.method == 'POST':
        # Get request data
        data = request.json
        print(f"Got request {data}")
        webserver.logger.info(
            f'Start /api/state_diff_from_mean with job_id {webserver.job_counter} and data {data}')

        if webserver.tasks_runner.shutdown_event.is_set():
            return jsonify({"job_id": "job_id_" + str(-1), "reason": "shutting down"})

        state = data.get('state')
        question = data.get('question')

        # Register job. Don't wait for task to finish
        task = (webserver.job_counter, webserver.data_ingestor.calculate_state_diff_from_mean,
                (state, question, ))
        webserver.tasks_runner.submit_task(task)

        # Increment job_id counter
        with webserver.job_id_lock:
            current_job_id = webserver.job_counter
            webserver.job_counter += 1

        # Return associated job_id
        webserver.logger.info('End /api/state_diff_from_mean')
        return jsonify({"job_id": "job_id_" + str(current_job_id)})
    # Else, Method Not Allowed
    webserver.logger.exception("Method not allowed in /api/state_diff_from_mean")
    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    if request.method == 'POST':
        # Get request data
        data = request.json
        print(f"Got request {data}")
        webserver.logger.info(
            f'Start /api/mean_by_category with job_id {webserver.job_counter} and data {data}')

        if webserver.tasks_runner.shutdown_event.is_set():
            return jsonify({"job_id": "job_id_" + str(-1), "reason": "shutting down"})

        question = data.get('question')

        # Register job. Don't wait for task to finish
        task = (webserver.job_counter, webserver.data_ingestor.calculate_mean_by_category,
                (question, ))
        webserver.tasks_runner.submit_task(task)

        # Increment job_id counter
        with webserver.job_id_lock:
            current_job_id = webserver.job_counter
            webserver.job_counter += 1

        # Return associated job_id
        webserver.logger.info('End /api/mean_by_category')
        return jsonify({"job_id": "job_id_" + str(current_job_id)})
    # Else, Method Not Allowed
    webserver.logger.exception("Method not allowed in /api/mean_by_category")
    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    if request.method == 'POST':
        # Get request data
        data = request.json
        print(f"Got request {data}")
        webserver.logger.info(
            f'Start /api/state_mean_by_category with {webserver.job_counter} and data {data}')

        if webserver.tasks_runner.shutdown_event.is_set():
            return jsonify({"job_id": "job_id_" + str(-1), "reason": "shutting down"})

        state = data.get('state')
        question = data.get('question')

        # Register job. Don't wait for task to finish
        task = (webserver.job_counter, webserver.data_ingestor.calculate_state_mean_by_category,
                (state, question, ))
        webserver.tasks_runner.submit_task(task)

        # Increment job_id counter
        with webserver.job_id_lock:
            current_job_id = webserver.job_counter
            webserver.job_counter += 1

        # Return associated job_id
        webserver.logger.info('End /api/state_mean_by_category')
        return jsonify({"job_id": "job_id_" + str(current_job_id)})
    # Else, Method Not Allowed
    webserver.logger.exception("Method not allowed in /api/state_mean_by_category")
    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/graceful_shutdown', methods=['GET'])
def graceful_shutdown():
    if request.method == 'GET':
        webserver.logger.info(
            f'Start /api/graceful_shutdown with job_id_{webserver.job_counter}')
 
        # Resetam job counter-ul
        webserver.job_counter = 1

        webserver.tasks_runner.graceful_shutdown()
        webserver.logger.info(f'End /api/jobs with job_id_{webserver.job_counter}')
        return jsonify({"job_id": "job_id_" + str(-1), "reason": "shutting down"})
    # Else, Method Not Allowed
    webserver.logger.exception("Method not allowed in /api/graceful_shutdown")
    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/jobs', methods=['GET'])
def get_jobs():
    if request.method == 'GET':
        webserver.logger.info(f'Start /api/jobs with job_id_{webserver.job_counter}')
        job_statuses = []
        for job_id in range(1, webserver.job_counter):
            job_status = webserver.tasks_runner.get_job_status(job_id)
            job_id_str = "job_id_" + str(job_id)
            job_statuses.append({job_id_str: job_status['status']})
        res_dict = {'status': 'done', 'data' : job_statuses}
        webserver.logger.info(f'End /api/jobs with the result: {res_dict}')
        return jsonify(res_dict)
    # Else, Method Not Allowed
    webserver.logger.exception("Method not allowed in /api/jobs")
    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/num_jobs', methods=['GET'])
def get_num_jobs():
    if request.method == 'GET':
        webserver.logger.info('Start /api/num_jobs')
        webserver.logger.info(f'Result of /api/num_jobs is {webserver.job_counter - 1}')
        count = 0
        for job_id in range(1, webserver.job_counter):
            job_status = webserver.tasks_runner.get_job_status(job_id)
            if job_status['status'] == 'running':
                count += 1
        return jsonify({'num_jobs': count})
    # Else, Method Not Allowed
    webserver.logger.exception("Method not allowed in /api/num_jobs")
    return jsonify({"error": "Method not allowed"}), 405

# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
    routes = get_defined_routes()
    msg = "Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg

def get_defined_routes():
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
